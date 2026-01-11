/**
 * Report Generator Service
 * Generates PDF and Word documents client-side
 */

import { jsPDF } from 'jspdf'
import { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, BorderStyle } from 'docx'
import { saveAs } from 'file-saver'

/**
 * Format a date string to a readable format
 */
function formatDate(dateStr, locale = 'de') {
  const date = new Date(dateStr)
  return date.toLocaleDateString(locale === 'de' ? 'de-DE' : 'en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

/**
 * Get the category name based on locale
 */
function getCategoryName(category, locale = 'de') {
  if (category.name_de && category.name_en) {
    return locale === 'de' ? category.name_de : category.name_en
  }
  return category.name || category.name_de || category.name_en || ''
}

/**
 * Get grade description for German school grades
 */
function getGradeDescription(grade) {
  const descriptions = {
    1: 'Very Good (Sehr gut)',
    2: 'Good (Gut)',
    3: 'Satisfactory (Befriedigend)',
    4: 'Adequate (Ausreichend)',
    5: 'Poor (Mangelhaft)',
    6: 'Very Poor (Ungenuegend)'
  }
  return descriptions[grade] || String(grade)
}

/**
 * Generate PDF report for a pupil
 * @param {Object} pupil - Pupil data { id, first_name, last_name, class_id }
 * @param {Array} entries - Array of entry objects
 * @param {Array} categories - Array of category objects
 * @param {string} startDate - Start date for report period
 * @param {string} endDate - End date for report period
 * @param {string} locale - Language locale ('de' or 'en')
 */
export function generatePDF(pupil, entries, categories, startDate, endDate, locale = 'de') {
  const doc = new jsPDF()
  const pageWidth = doc.internal.pageSize.getWidth()
  const margin = 20
  let yPos = 20

  // Localized strings
  const strings = locale === 'de' ? {
    title: 'Entwicklungsbericht',
    reportPeriod: 'Berichtszeitraum',
    generated: 'Erstellt am',
    summary: 'Zusammenfassung',
    totalEntries: 'Eintraege gesamt',
    averageGrade: 'Durchschnittsnote',
    entriesByCategory: 'Eintraege nach Kategorie',
    grade: 'Note',
    page: 'Seite',
    of: 'von'
  } : {
    title: 'Development Report',
    reportPeriod: 'Report Period',
    generated: 'Generated',
    summary: 'Summary',
    totalEntries: 'Total Entries',
    averageGrade: 'Average Grade',
    entriesByCategory: 'Entries by Category',
    grade: 'Grade',
    page: 'Page',
    of: 'of'
  }

  // Title
  doc.setFontSize(18)
  doc.setFont('helvetica', 'bold')
  doc.text(strings.title, pageWidth / 2, yPos, { align: 'center' })
  yPos += 10

  doc.setFontSize(14)
  doc.text(`${pupil.first_name} ${pupil.last_name}`, pageWidth / 2, yPos, { align: 'center' })
  yPos += 15

  // Report period
  doc.setFontSize(10)
  doc.setFont('helvetica', 'normal')
  doc.text(`${strings.reportPeriod}: ${formatDate(startDate, locale)} - ${formatDate(endDate, locale)}`, margin, yPos)
  yPos += 5
  doc.text(`${strings.generated}: ${formatDate(new Date().toISOString(), locale)}`, margin, yPos)
  yPos += 15

  // Summary section
  doc.setFontSize(12)
  doc.setFont('helvetica', 'bold')
  doc.text(strings.summary, margin, yPos)
  yPos += 8

  doc.setFontSize(10)
  doc.setFont('helvetica', 'normal')
  doc.text(`${strings.totalEntries}: ${entries.length}`, margin, yPos)
  yPos += 5

  if (entries.length > 0) {
    const avgGrade = entries.reduce((sum, e) => sum + e.grade, 0) / entries.length
    doc.text(`${strings.averageGrade}: ${avgGrade.toFixed(2)}`, margin, yPos)
    yPos += 15
  } else {
    yPos += 10
  }

  // Entries by category
  doc.setFontSize(12)
  doc.setFont('helvetica', 'bold')
  doc.text(strings.entriesByCategory, margin, yPos)
  yPos += 10

  // Group entries by category
  const entriesByCategory = {}
  entries.forEach(entry => {
    const catId = entry.category_id
    if (!entriesByCategory[catId]) {
      entriesByCategory[catId] = []
    }
    entriesByCategory[catId].push(entry)
  })

  // Draw entries table for each category
  categories.forEach(category => {
    const catEntries = entriesByCategory[category.id] || []
    if (catEntries.length === 0) return

    // Check if we need a new page
    if (yPos > 250) {
      doc.addPage()
      yPos = 20
    }

    doc.setFontSize(11)
    doc.setFont('helvetica', 'bold')
    doc.text(getCategoryName(category, locale), margin, yPos)
    yPos += 7

    doc.setFontSize(9)
    doc.setFont('helvetica', 'normal')

    catEntries.forEach(entry => {
      // Check if we need a new page
      if (yPos > 270) {
        doc.addPage()
        yPos = 20
      }

      const dateText = formatDate(entry.date, locale)
      const gradeText = `${strings.grade}: ${entry.grade}`

      doc.setFont('helvetica', 'bold')
      doc.text(`${dateText} - ${gradeText}`, margin + 5, yPos)
      yPos += 5

      if (entry.notes) {
        doc.setFont('helvetica', 'normal')
        // Word wrap notes
        const lines = doc.splitTextToSize(entry.notes, pageWidth - margin * 2 - 10)
        lines.forEach(line => {
          if (yPos > 270) {
            doc.addPage()
            yPos = 20
          }
          doc.text(line, margin + 5, yPos)
          yPos += 4
        })
      }
      yPos += 3
    })
    yPos += 5
  })

  // Footer
  const pageCount = doc.getNumberOfPages()
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i)
    doc.setFontSize(8)
    doc.setFont('helvetica', 'normal')
    doc.text(
      `${strings.page} ${i} ${strings.of} ${pageCount}`,
      pageWidth / 2,
      doc.internal.pageSize.getHeight() - 10,
      { align: 'center' }
    )
  }

  // Save the PDF
  const filename = `${pupil.first_name}_${pupil.last_name}_Report_${startDate}_${endDate}.pdf`
  doc.save(filename)
}

/**
 * Generate Word document report for a pupil
 * @param {Object} pupil - Pupil data { id, first_name, last_name, class_id }
 * @param {Array} entries - Array of entry objects
 * @param {Array} categories - Array of category objects
 * @param {string} startDate - Start date for report period
 * @param {string} endDate - End date for report period
 * @param {string} locale - Language locale ('de' or 'en')
 */
export async function generateWord(pupil, entries, categories, startDate, endDate, locale = 'de') {
  // Localized strings
  const strings = locale === 'de' ? {
    title: 'Entwicklungsbericht',
    reportPeriod: 'Berichtszeitraum',
    generated: 'Erstellt am',
    summary: 'Zusammenfassung',
    totalEntries: 'Eintraege gesamt',
    averageGrade: 'Durchschnittsnote',
    entriesByCategory: 'Eintraege nach Kategorie',
    date: 'Datum',
    grade: 'Note',
    notes: 'Notizen'
  } : {
    title: 'Development Report',
    reportPeriod: 'Report Period',
    generated: 'Generated',
    summary: 'Summary',
    totalEntries: 'Total Entries',
    averageGrade: 'Average Grade',
    entriesByCategory: 'Entries by Category',
    date: 'Date',
    grade: 'Grade',
    notes: 'Notes'
  }

  const children = []

  // Title
  children.push(
    new Paragraph({
      text: strings.title,
      heading: HeadingLevel.HEADING_1,
      alignment: 'center'
    })
  )

  children.push(
    new Paragraph({
      text: `${pupil.first_name} ${pupil.last_name}`,
      heading: HeadingLevel.HEADING_2,
      alignment: 'center'
    })
  )

  children.push(new Paragraph({ text: '' }))

  // Report period
  children.push(
    new Paragraph({
      children: [
        new TextRun({ text: `${strings.reportPeriod}: `, bold: true }),
        new TextRun({ text: `${formatDate(startDate, locale)} - ${formatDate(endDate, locale)}` })
      ]
    })
  )

  children.push(
    new Paragraph({
      children: [
        new TextRun({ text: `${strings.generated}: `, bold: true }),
        new TextRun({ text: formatDate(new Date().toISOString(), locale) })
      ]
    })
  )

  children.push(new Paragraph({ text: '' }))

  // Summary
  children.push(
    new Paragraph({
      text: strings.summary,
      heading: HeadingLevel.HEADING_2
    })
  )

  children.push(
    new Paragraph({
      children: [
        new TextRun({ text: `${strings.totalEntries}: `, bold: true }),
        new TextRun({ text: String(entries.length) })
      ]
    })
  )

  if (entries.length > 0) {
    const avgGrade = entries.reduce((sum, e) => sum + e.grade, 0) / entries.length
    children.push(
      new Paragraph({
        children: [
          new TextRun({ text: `${strings.averageGrade}: `, bold: true }),
          new TextRun({ text: avgGrade.toFixed(2) })
        ]
      })
    )
  }

  children.push(new Paragraph({ text: '' }))

  // Entries by category
  children.push(
    new Paragraph({
      text: strings.entriesByCategory,
      heading: HeadingLevel.HEADING_2
    })
  )

  // Group entries by category
  const entriesByCategory = {}
  entries.forEach(entry => {
    const catId = entry.category_id
    if (!entriesByCategory[catId]) {
      entriesByCategory[catId] = []
    }
    entriesByCategory[catId].push(entry)
  })

  // Create table for entries
  categories.forEach(category => {
    const catEntries = entriesByCategory[category.id] || []
    if (catEntries.length === 0) return

    children.push(new Paragraph({ text: '' }))
    children.push(
      new Paragraph({
        text: getCategoryName(category, locale),
        heading: HeadingLevel.HEADING_3
      })
    )

    // Create table
    const tableRows = [
      new TableRow({
        children: [
          new TableCell({
            children: [new Paragraph({ children: [new TextRun({ text: strings.date, bold: true })] })],
            width: { size: 20, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({ children: [new TextRun({ text: strings.grade, bold: true })] })],
            width: { size: 15, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({ children: [new TextRun({ text: strings.notes, bold: true })] })],
            width: { size: 65, type: WidthType.PERCENTAGE }
          })
        ]
      })
    ]

    catEntries.forEach(entry => {
      tableRows.push(
        new TableRow({
          children: [
            new TableCell({
              children: [new Paragraph({ text: formatDate(entry.date, locale) })]
            }),
            new TableCell({
              children: [new Paragraph({ text: String(entry.grade) })]
            }),
            new TableCell({
              children: [new Paragraph({ text: entry.notes || '' })]
            })
          ]
        })
      )
    })

    children.push(
      new Table({
        rows: tableRows,
        width: { size: 100, type: WidthType.PERCENTAGE }
      })
    )
  })

  // Create document
  const doc = new Document({
    sections: [{
      properties: {},
      children: children
    }]
  })

  // Generate and save
  const blob = await Packer.toBlob(doc)
  const filename = `${pupil.first_name}_${pupil.last_name}_Report_${startDate}_${endDate}.docx`
  saveAs(blob, filename)
}
