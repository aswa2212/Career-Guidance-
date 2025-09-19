import { motion } from 'framer-motion'
import useAppStore from '../store/useAppStore'

const ProgressBar = ({ 
  progress = 0, 
  className = '', 
  showPercentage = true, 
  color = 'primary',
  size = 'md',
  animated = true 
}) => {
  const { isDarkMode } = useAppStore()
  
  const colors = {
    primary: 'bg-primary',
    secondary: 'bg-secondary',
    accent: 'bg-accent',
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    danger: 'bg-red-500'
  }
  
  const sizes = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4'
  }
  
  const clampedProgress = Math.min(Math.max(progress, 0), 100)
  
  return (
    <div className={`w-full ${className}`}>
      {showPercentage && (
        <div className={`flex justify-between items-center mb-2 text-sm font-medium ${
          isDarkMode ? 'text-gray-300' : 'text-gray-700'
        }`}>
          <span>Progress</span>
          <span>{Math.round(clampedProgress)}%</span>
        </div>
      )}
      
      <div className={`w-full ${sizes[size]} ${
        isDarkMode ? 'bg-gray-700' : 'bg-gray-200'
      } rounded-full overflow-hidden`}>
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${clampedProgress}%` }}
          transition={{ 
            duration: animated ? 0.8 : 0,
            ease: "easeOut" 
          }}
          className={`${sizes[size]} ${colors[color]} rounded-full relative overflow-hidden`}
        >
          {animated && (
            <motion.div
              className="absolute inset-0 bg-white/20"
              animate={{
                x: ['-100%', '100%']
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: "linear"
              }}
            />
          )}
        </motion.div>
      </div>
    </div>
  )
}

export default ProgressBar
