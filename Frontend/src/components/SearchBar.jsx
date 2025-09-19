import { useState } from 'react'
import { Search, X } from 'lucide-react'
import { motion } from 'framer-motion'
import useAppStore from '../store/useAppStore'

const SearchBar = ({ 
  placeholder = "Search courses, colleges, resources...", 
  onSearch, 
  className = '',
  showClearButton = true 
}) => {
  const { searchQuery, setSearchQuery, isDarkMode } = useAppStore()
  const [isFocused, setIsFocused] = useState(false)

  const handleSearch = (e) => {
    e.preventDefault()
    if (onSearch) {
      onSearch(searchQuery)
    }
  }

  const handleClear = () => {
    setSearchQuery('')
    if (onSearch) {
      onSearch('')
    }
  }

  return (
    <motion.form
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2 }}
      onSubmit={handleSearch}
      className={`relative ${className}`}
    >
      <div className={`relative flex items-center ${isDarkMode ? 'bg-gray-800' : 'bg-white'} rounded-2xl border-2 transition-all duration-300 ${
        isFocused 
          ? 'border-primary shadow-lg shadow-primary/10' 
          : isDarkMode 
            ? 'border-gray-700 hover:border-gray-600' 
            : 'border-gray-200 hover:border-gray-300'
      }`}>
        <Search className={`absolute left-4 w-5 h-5 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`} />
        
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder={placeholder}
          className={`w-full pl-12 pr-12 py-3 bg-transparent rounded-2xl focus:outline-none ${
            isDarkMode ? 'text-white placeholder-gray-400' : 'text-gray-900 placeholder-gray-500'
          }`}
          aria-label="Search"
        />
        
        {searchQuery && showClearButton && (
          <motion.button
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            type="button"
            onClick={handleClear}
            className={`absolute right-4 p-1 rounded-full hover:bg-gray-100 ${
              isDarkMode ? 'hover:bg-gray-700 text-gray-400' : 'text-gray-500'
            } transition-colors duration-200`}
            aria-label="Clear search"
          >
            <X className="w-4 h-4" />
          </motion.button>
        )}
      </div>
    </motion.form>
  )
}

export default SearchBar
