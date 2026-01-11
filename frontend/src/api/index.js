/**
 * API Layer for Pupil Development Tracker
 * Wraps localStorage operations with Promise-based interface
 * to maintain compatibility with existing components
 */

import {
  initializeStorage,
  getSchoolYears as storageGetSchoolYears,
  getSchoolYear as storageGetSchoolYear,
  createSchoolYear as storageCreateSchoolYear,
  updateSchoolYear as storageUpdateSchoolYear,
  deleteSchoolYear as storageDeleteSchoolYear,
  getClasses as storageGetClasses,
  getClass as storageGetClass,
  createClass as storageCreateClass,
  updateClass as storageUpdateClass,
  deleteClass as storageDeleteClass,
  getPupils as storageGetPupils,
  getPupil as storageGetPupil,
  createPupil as storageCreatePupil,
  updatePupil as storageUpdatePupil,
  deletePupil as storageDeletePupil,
  getCategories as storageGetCategories,
  getCategory as storageGetCategory,
  createCategory as storageCreateCategory,
  updateCategory as storageUpdateCategory,
  deleteCategory as storageDeleteCategory,
  getEntries as storageGetEntries,
  getEntry as storageGetEntry,
  getEntriesForPupil as storageGetEntriesForPupil,
  createEntry as storageCreateEntry,
  updateEntry as storageUpdateEntry,
  deleteEntry as storageDeleteEntry,
  exportAllData,
  exportEntriesAsCsv,
  importData
} from '../storage'

// Initialize storage on import
initializeStorage()

// Helper to wrap sync operations in promise and return { data } format
function wrapPromise(fn) {
  return (...args) => {
    return new Promise((resolve) => {
      const result = fn(...args)
      resolve({ data: result })
    })
  }
}

// School Years
export const getSchoolYears = wrapPromise(storageGetSchoolYears)
export const getSchoolYear = wrapPromise(storageGetSchoolYear)
export const createSchoolYear = wrapPromise(storageCreateSchoolYear)
export const updateSchoolYear = wrapPromise((id, data) => storageUpdateSchoolYear(id, data))
export const deleteSchoolYear = wrapPromise(storageDeleteSchoolYear)

// Classes
export const getClasses = wrapPromise(storageGetClasses)
export const getClass = wrapPromise(storageGetClass)
export const createClass = wrapPromise(storageCreateClass)
export const updateClass = wrapPromise((id, data) => storageUpdateClass(id, data))
export const deleteClass = wrapPromise(storageDeleteClass)

// Pupils
export const getPupils = wrapPromise(storageGetPupils)
export const getPupil = wrapPromise(storageGetPupil)
export const createPupil = wrapPromise(storageCreatePupil)
export const updatePupil = wrapPromise((id, data) => storageUpdatePupil(id, data))
export const deletePupil = wrapPromise(storageDeletePupil)

// Categories
export const getCategories = wrapPromise(storageGetCategories)
export const getCategory = wrapPromise(storageGetCategory)
export const createCategory = wrapPromise(storageCreateCategory)
export const updateCategory = wrapPromise((id, data) => storageUpdateCategory(id, data))
export const deleteCategory = wrapPromise(storageDeleteCategory)

// Entries
export const getEntries = wrapPromise(storageGetEntries)
export const getEntry = wrapPromise(storageGetEntry)
export const getEntriesForPupil = wrapPromise(storageGetEntriesForPupil)
export const createEntry = wrapPromise(storageCreateEntry)
export const updateEntry = wrapPromise((id, data) => storageUpdateEntry(id, data))
export const deleteEntry = wrapPromise(storageDeleteEntry)

// Export/Import
export const exportJson = wrapPromise(exportAllData)
export const exportCsv = wrapPromise(exportEntriesAsCsv)
export const importJson = wrapPromise(importData)

// These functions are no longer needed for backend URLs
// but kept for backwards compatibility - they return null
export function downloadPupilPdf(pupilId, startDate, endDate) {
  // No longer used - client-side PDF generation handles this
  return null
}

export function downloadPupilDocx(pupilId, startDate, endDate) {
  // No longer used - client-side DOCX generation handles this
  return null
}
