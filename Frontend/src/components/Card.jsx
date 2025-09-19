import { motion } from 'framer-motion'
import useAppStore from '../store/useAppStore'

const Card = ({ 
  children, 
  className = '', 
  hover = true, 
  glassmorphism = false,
  onClick,
  ...props 
}) => {
  const { isDarkMode } = useAppStore()
  
  const baseClasses = 'rounded-2xl transition-all duration-300 border'
  
  const getCardClasses = () => {
    if (glassmorphism) {
      return isDarkMode ? 'glassmorphism-dark' : 'glassmorphism'
    }
    return isDarkMode ? 'card-dark' : 'card'
  }
  
  const hoverClasses = hover ? 'hover:shadow-xl hover:-translate-y-1' : ''
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={hover ? { y: -4 } : {}}
      className={`${baseClasses} ${getCardClasses()} ${hoverClasses} ${className}`}
      onClick={onClick}
      {...props}
    >
      {children}
    </motion.div>
  )
}

export default Card
