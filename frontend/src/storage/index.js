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
  { id: 1, name: 'Work Behavior / Arbeitsverhalten', is_custom: false },
  { id: 2, name: 'Social Behavior / Sozialverhalten', is_custom: false },
  { id: 3, name: 'Learning Development / Lernentwicklung', is_custom: false },
  { id: 4, name: 'Special Incidents / Besondere Vorkommnisse', is_custom: false },
  { id: 5, name: 'Motor Skills / Motorik', is_custom: false },
  { id: 6, name: 'Creativity / Kreativitaet', is_custom: false },
  { id: 7, name: 'Language Development / Sprachentwicklung', is_custom: false },
  { id: 8, name: 'Independence / Selbststaendigkeit', is_custom: false }
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
    return [
      entry.date,
      pupil?.first_name || '',
      pupil?.last_name || '',
      cls?.name || '',
      category?.name || '',
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
