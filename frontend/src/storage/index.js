/**
 * LocalStorage Service for Pupil Development Tracker
 * Provides CRUD operations for all data entities
 */

const STORAGE_KEYS = {
  SCHOOL_YEARS: 'pupil_tracker_school_years',
  CLASSES: 'pupil_tracker_classes',
  PUPILS: 'pupil_tracker_pupils',
  CATEGORIES: 'pupil_tracker_categories',
  ENTRIES: 'pupil_tracker_entries',
  INITIALIZED: 'pupil_tracker_initialized'
}

// Predefined categories (built-in)
const DEFAULT_CATEGORIES = [
  { id: 1, name_de: 'Arbeitsverhalten', name_en: 'Work Behavior', is_custom: false },
  { id: 2, name_de: 'Sozialverhalten', name_en: 'Social Behavior', is_custom: false },
  { id: 3, name_de: 'Lernentwicklung', name_en: 'Learning Development', is_custom: false },
  { id: 4, name_de: 'Besondere Vorkommnisse', name_en: 'Special Incidents', is_custom: false },
  { id: 5, name_de: 'Motorik', name_en: 'Motor Skills', is_custom: false },
  { id: 6, name_de: 'Kreativitaet', name_en: 'Creativity', is_custom: false },
  { id: 7, name_de: 'Sprachentwicklung', name_en: 'Language Development', is_custom: false },
  { id: 8, name_de: 'Selbststaendigkeit', name_en: 'Independence', is_custom: false }
]

// Generate unique ID
function generateId() {
  return Date.now() + Math.floor(Math.random() * 1000)
}

// Generic storage helpers
function getStorage(key) {
  const data = localStorage.getItem(key)
  return data ? JSON.parse(data) : []
}

function setStorage(key, data) {
  localStorage.setItem(key, JSON.stringify(data))
}

// Migrate old category format to new format
function migrateCategories() {
  const categories = getStorage(STORAGE_KEYS.CATEGORIES)
  let needsUpdate = false

  const migrated = categories.map(cat => {
    // If category has old combined 'name' format like "Work Behavior / Arbeitsverhalten"
    if (cat.name && cat.name.includes(' / ')) {
      needsUpdate = true
      const [en, de] = cat.name.split(' / ')
      return { ...cat, name_en: en, name_de: de, name: undefined }
    }
    // If category only has 'name' without slash, try to find matching default
    if (cat.name && !cat.name_de && !cat.name_en) {
      needsUpdate = true
      const defaultCat = DEFAULT_CATEGORIES.find(d =>
        d.name_de === cat.name || d.name_en === cat.name
      )
      if (defaultCat) {
        return { ...cat, name_de: defaultCat.name_de, name_en: defaultCat.name_en, name: undefined }
      }
      // For custom categories, use the name for both
      return { ...cat, name_de: cat.name, name_en: cat.name, name: undefined }
    }
    return cat
  })

  if (needsUpdate) {
    setStorage(STORAGE_KEYS.CATEGORIES, migrated)
  }

  // Also ensure all default categories exist with correct format
  const existingIds = migrated.map(c => c.id)
  const missingDefaults = DEFAULT_CATEGORIES.filter(d => !existingIds.includes(d.id))
  if (missingDefaults.length > 0) {
    setStorage(STORAGE_KEYS.CATEGORIES, [...migrated, ...missingDefaults])
  }
}

// Initialize storage with default data on first load
export function initializeStorage() {
  const initialized = localStorage.getItem(STORAGE_KEYS.INITIALIZED)
  if (!initialized) {
    setStorage(STORAGE_KEYS.SCHOOL_YEARS, [])
    setStorage(STORAGE_KEYS.CLASSES, [])
    setStorage(STORAGE_KEYS.PUPILS, [])
    setStorage(STORAGE_KEYS.CATEGORIES, DEFAULT_CATEGORIES)
    setStorage(STORAGE_KEYS.ENTRIES, [])
    localStorage.setItem(STORAGE_KEYS.INITIALIZED, 'true')
  }

  // Always run migration to fix old category formats
  migrateCategories()
}

// School Years
export function getSchoolYears() {
  return getStorage(STORAGE_KEYS.SCHOOL_YEARS)
}

export function getSchoolYear(id) {
  const years = getSchoolYears()
  return years.find(y => y.id === Number(id))
}

export function createSchoolYear(data) {
  const years = getSchoolYears()
  const newYear = { id: generateId(), ...data }
  years.push(newYear)
  setStorage(STORAGE_KEYS.SCHOOL_YEARS, years)
  return newYear
}

export function updateSchoolYear(id, data) {
  const years = getSchoolYears()
  const index = years.findIndex(y => y.id === Number(id))
  if (index !== -1) {
    years[index] = { ...years[index], ...data }
    setStorage(STORAGE_KEYS.SCHOOL_YEARS, years)
    return years[index]
  }
  return null
}

export function deleteSchoolYear(id) {
  const years = getSchoolYears()
  const filtered = years.filter(y => y.id !== Number(id))
  setStorage(STORAGE_KEYS.SCHOOL_YEARS, filtered)
  return true
}

// Classes
export function getClasses() {
  return getStorage(STORAGE_KEYS.CLASSES)
}

export function getClass(id) {
  const classes = getClasses()
  return classes.find(c => c.id === Number(id))
}

export function createClass(data) {
  const classes = getClasses()
  const newClass = { id: generateId(), ...data }
  classes.push(newClass)
  setStorage(STORAGE_KEYS.CLASSES, classes)
  return newClass
}

export function updateClass(id, data) {
  const classes = getClasses()
  const index = classes.findIndex(c => c.id === Number(id))
  if (index !== -1) {
    classes[index] = { ...classes[index], ...data }
    setStorage(STORAGE_KEYS.CLASSES, classes)
    return classes[index]
  }
  return null
}

export function deleteClass(id) {
  const classes = getClasses()
  const filtered = classes.filter(c => c.id !== Number(id))
  setStorage(STORAGE_KEYS.CLASSES, filtered)
  // Also delete all pupils in this class
  const pupils = getPupils()
  const filteredPupils = pupils.filter(p => p.class_id !== Number(id))
  setStorage(STORAGE_KEYS.PUPILS, filteredPupils)
  // Delete entries for those pupils
  const deletedPupilIds = pupils.filter(p => p.class_id === Number(id)).map(p => p.id)
  const entries = getEntries()
  const filteredEntries = entries.filter(e => !deletedPupilIds.includes(e.pupil_id))
  setStorage(STORAGE_KEYS.ENTRIES, filteredEntries)
  return true
}

// Pupils
export function getPupils() {
  return getStorage(STORAGE_KEYS.PUPILS)
}

export function getPupil(id) {
  const pupils = getPupils()
  return pupils.find(p => p.id === Number(id))
}

export function createPupil(data) {
  const pupils = getPupils()
  const newPupil = { id: generateId(), ...data }
  pupils.push(newPupil)
  setStorage(STORAGE_KEYS.PUPILS, pupils)
  return newPupil
}

export function updatePupil(id, data) {
  const pupils = getPupils()
  const index = pupils.findIndex(p => p.id === Number(id))
  if (index !== -1) {
    pupils[index] = { ...pupils[index], ...data }
    setStorage(STORAGE_KEYS.PUPILS, pupils)
    return pupils[index]
  }
  return null
}

export function deletePupil(id) {
  const pupils = getPupils()
  const filtered = pupils.filter(p => p.id !== Number(id))
  setStorage(STORAGE_KEYS.PUPILS, filtered)
  // Also delete all entries for this pupil
  const entries = getEntries()
  const filteredEntries = entries.filter(e => e.pupil_id !== Number(id))
  setStorage(STORAGE_KEYS.ENTRIES, filteredEntries)
  return true
}

// Categories
export function getCategories() {
  return getStorage(STORAGE_KEYS.CATEGORIES)
}

export function getCategory(id) {
  const categories = getCategories()
  return categories.find(c => c.id === Number(id))
}

export function createCategory(data) {
  const categories = getCategories()
  const newCategory = { id: generateId(), is_custom: true, ...data }
  categories.push(newCategory)
  setStorage(STORAGE_KEYS.CATEGORIES, categories)
  return newCategory
}

export function updateCategory(id, data) {
  const categories = getCategories()
  const index = categories.findIndex(c => c.id === Number(id))
  if (index !== -1) {
    categories[index] = { ...categories[index], ...data }
    setStorage(STORAGE_KEYS.CATEGORIES, categories)
    return categories[index]
  }
  return null
}

export function deleteCategory(id) {
  const categories = getCategories()
  const category = categories.find(c => c.id === Number(id))
  // Only allow deleting custom categories
  if (category && category.is_custom) {
    const filtered = categories.filter(c => c.id !== Number(id))
    setStorage(STORAGE_KEYS.CATEGORIES, filtered)
    return true
  }
  return false
}

// Entries
export function getEntries() {
  return getStorage(STORAGE_KEYS.ENTRIES)
}

export function getEntry(id) {
  const entries = getEntries()
  return entries.find(e => e.id === Number(id))
}

export function getEntriesForPupil(pupilId) {
  const entries = getEntries()
  return entries.filter(e => e.pupil_id === Number(pupilId))
}

export function createEntry(data) {
  const entries = getEntries()
  const newEntry = {
    id: generateId(),
    created_at: new Date().toISOString(),
    ...data
  }
  entries.push(newEntry)
  setStorage(STORAGE_KEYS.ENTRIES, entries)
  return newEntry
}

export function updateEntry(id, data) {
  const entries = getEntries()
  const index = entries.findIndex(e => e.id === Number(id))
  if (index !== -1) {
    entries[index] = {
      ...entries[index],
      ...data,
      updated_at: new Date().toISOString()
    }
    setStorage(STORAGE_KEYS.ENTRIES, entries)
    return entries[index]
  }
  return null
}

export function deleteEntry(id) {
  const entries = getEntries()
  const filtered = entries.filter(e => e.id !== Number(id))
  setStorage(STORAGE_KEYS.ENTRIES, filtered)
  return true
}

// Export all data as JSON
export function exportAllData() {
  return {
    schoolYears: getSchoolYears(),
    classes: getClasses(),
    pupils: getPupils(),
    categories: getCategories(),
    entries: getEntries(),
    exportedAt: new Date().toISOString()
  }
}

// Export entries as CSV
export function exportEntriesAsCsv() {
  const entries = getEntries()
  const pupils = getPupils()
  const categories = getCategories()
  const classes = getClasses()

  const headers = ['Date', 'Pupil First Name', 'Pupil Last Name', 'Class', 'Category', 'Grade', 'Notes']
  const rows = entries.map(entry => {
    const pupil = pupils.find(p => p.id === entry.pupil_id)
    const category = categories.find(c => c.id === entry.category_id)
    const cls = pupil ? classes.find(c => c.id === pupil.class_id) : null
    const categoryName = category ? (category.name_en || category.name || '') : ''
    return [
      entry.date,
      pupil?.first_name || '',
      pupil?.last_name || '',
      cls?.name || '',
      categoryName,
      entry.grade,
      (entry.notes || '').replace(/"/g, '""')
    ].map(val => `"${val}"`).join(',')
  })

  return [headers.join(','), ...rows].join('\n')
}

// Import data from JSON
export function importData(data) {
  if (data.schoolYears) {
    setStorage(STORAGE_KEYS.SCHOOL_YEARS, data.schoolYears)
  }
  if (data.classes) {
    setStorage(STORAGE_KEYS.CLASSES, data.classes)
  }
  if (data.pupils) {
    setStorage(STORAGE_KEYS.PUPILS, data.pupils)
  }
  if (data.categories) {
    // Merge with default categories, keeping custom ones
    const defaultIds = DEFAULT_CATEGORIES.map(c => c.id)
    const customCategories = data.categories.filter(c => !defaultIds.includes(c.id) || c.is_custom)
    const merged = [...DEFAULT_CATEGORIES, ...customCategories.filter(c => c.is_custom)]
    setStorage(STORAGE_KEYS.CATEGORIES, merged)
  }
  if (data.entries) {
    setStorage(STORAGE_KEYS.ENTRIES, data.entries)
  }
  return true
}

// Clear all data (for testing or reset)
export function clearAllData() {
  localStorage.removeItem(STORAGE_KEYS.SCHOOL_YEARS)
  localStorage.removeItem(STORAGE_KEYS.CLASSES)
  localStorage.removeItem(STORAGE_KEYS.PUPILS)
  localStorage.removeItem(STORAGE_KEYS.CATEGORIES)
  localStorage.removeItem(STORAGE_KEYS.ENTRIES)
  localStorage.removeItem(STORAGE_KEYS.INITIALIZED)
}

// Seed test data for development and demonstration
export function seedTestData() {
  // Check if data already exists
  const existingClasses = getClasses()
  const existingPupils = getPupils()
  if (existingClasses.length > 0 || existingPupils.length > 0) {
    return false // Data already exists, don't overwrite
  }

  // German first names
  const firstNames = [
    'Emma', 'Liam', 'Mia', 'Noah', 'Hannah', 'Ben', 'Lea', 'Finn', 'Anna', 'Leon',
    'Sophie', 'Elias', 'Marie', 'Paul', 'Emilia', 'Felix', 'Lina', 'Jonas', 'Mila', 'Lukas',
    'Charlotte', 'Maximilian', 'Amelie', 'Henry', 'Ella', 'Tim', 'Clara', 'David', 'Laura', 'Moritz',
    'Johanna', 'Alexander', 'Sarah', 'Julian', 'Emily', 'Niklas', 'Lena', 'Philipp', 'Nele', 'Jan'
  ]

  // German last names
  const lastNames = [
    'Mueller', 'Schmidt', 'Fischer', 'Weber', 'Meyer', 'Wagner', 'Becker', 'Schulz', 'Hoffmann', 'Koch',
    'Richter', 'Klein', 'Wolf', 'Schroeder', 'Neumann', 'Schwarz', 'Zimmermann', 'Braun', 'Hartmann', 'Krueger'
  ]

  // Sample observation texts in German
  const observationTexts = [
    'Zeigt gute Mitarbeit im Unterricht',
    'Hat heute beim Gruppenprojekt sehr gut kooperiert',
    'Braucht mehr Uebung bei Mathematik',
    'Sehr kreativ beim Kunstunterricht',
    'Hat Schwierigkeiten bei der Konzentration',
    'Loest Aufgaben selbststaendig und zuverlaessig',
    'Beteiligt sich aktiv an Klassendiskussionen',
    'Zeigt gute Fortschritte beim Lesen',
    'Ist hilfsbereit gegenueber Mitschuelern',
    'Hat die Hausaufgaben vollstaendig und ordentlich erledigt',
    'Zeigt Interesse an naturwissenschaftlichen Themen',
    'Konnte heute eine schwierige Aufgabe erfolgreich loesen',
    'Braucht Unterstuetzung bei schriftlichen Arbeiten',
    'Hat ein tolles Referat gehalten',
    'Zeigt verbesserte Feinmotorik beim Schreiben',
    'Arbeitet gut im Team zusammen',
    'Hat heute besonders aufmerksam zugehoert',
    'Zeigt Fortschritte in der Rechtschreibung',
    'Ist respektvoll im Umgang mit anderen',
    'Hat kreative Loesungsansaetze gezeigt',
    'Benoetigt mehr Zeit bei Textaufgaben',
    'Zeigt gutes Verstaendnis fuer Sachverhalte',
    'Hat heute sehr fleissig gearbeitet',
    'Kann Erlerntes gut anwenden',
    'Zeigt Eigeninitiative beim Lernen'
  ]

  // Create school years
  const schoolYears = [
    { id: 1001, name: '2023/2024', is_active: false },
    { id: 1002, name: '2024/2025', is_active: true }
  ]
  setStorage(STORAGE_KEYS.SCHOOL_YEARS, schoolYears)

  // Create classes (all in 2024/2025)
  const classes = [
    { id: 2001, name: 'Klasse 1a', school_year_id: 1002 },
    { id: 2002, name: 'Klasse 2b', school_year_id: 1002 },
    { id: 2003, name: 'Klasse 3c', school_year_id: 1002 },
    { id: 2004, name: 'Klasse 4d', school_year_id: 1002 }
  ]
  setStorage(STORAGE_KEYS.CLASSES, classes)

  // Create pupils (10 per class = 40 total)
  const pupils = []
  let pupilId = 3001
  let nameIndex = 0

  classes.forEach(cls => {
    for (let i = 0; i < 10; i++) {
      const firstName = firstNames[nameIndex % firstNames.length]
      const lastName = lastNames[nameIndex % lastNames.length]
      pupils.push({
        id: pupilId++,
        first_name: firstName,
        last_name: lastName,
        class_id: cls.id
      })
      nameIndex++
    }
  })
  setStorage(STORAGE_KEYS.PUPILS, pupils)

  // Create entries (3-5 per pupil = 120-200 entries)
  const entries = []
  let entryId = 4001
  const categoryIds = [1, 2, 3, 4, 5, 6, 7, 8] // All default category IDs

  // Date range: September 2024 - January 2025
  const startDate = new Date('2024-09-02')
  const endDate = new Date('2025-01-15')
  const dateRange = endDate.getTime() - startDate.getTime()

  pupils.forEach(pupil => {
    const numEntries = 3 + Math.floor(Math.random() * 3) // 3 to 5 entries

    for (let i = 0; i < numEntries; i++) {
      // Random date in range
      const randomTime = startDate.getTime() + Math.random() * dateRange
      const entryDate = new Date(randomTime)
      const dateStr = entryDate.toISOString().split('T')[0]

      // Random category
      const categoryId = categoryIds[Math.floor(Math.random() * categoryIds.length)]

      // Random grade (1-6, weighted toward better grades)
      const gradeRand = Math.random()
      let grade
      if (gradeRand < 0.3) grade = 1
      else if (gradeRand < 0.5) grade = 2
      else if (gradeRand < 0.7) grade = 3
      else if (gradeRand < 0.85) grade = 4
      else if (gradeRand < 0.95) grade = 5
      else grade = 6

      // Random notes (some entries have notes, some don't)
      const hasNotes = Math.random() > 0.2 // 80% have notes
      const notes = hasNotes
        ? observationTexts[Math.floor(Math.random() * observationTexts.length)]
        : ''

      entries.push({
        id: entryId++,
        pupil_id: pupil.id,
        category_id: categoryId,
        date: dateStr,
        grade: grade,
        notes: notes,
        created_at: new Date().toISOString()
      })
    }
  })
  setStorage(STORAGE_KEYS.ENTRIES, entries)

  return true
}
