import { z } from 'zod';

// Authentication schemas
export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),
  password: z
    .string()
    .min(1, 'Password is required')
    .min(6, 'Password must be at least 6 characters'),
});

export const registerSchema = z.object({
  full_name: z
    .string()
    .min(1, 'Full name is required')
    .min(2, 'Full name must be at least 2 characters')
    .max(100, 'Full name must be less than 100 characters'),
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),
  password: z
    .string()
    .min(1, 'Password is required')
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'Password must contain at least one uppercase letter, one lowercase letter, and one number'),
  confirmPassword: z
    .string()
    .min(1, 'Please confirm your password'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

// Profile schemas
export const profileSchema = z.object({
  full_name: z
    .string()
    .min(1, 'Full name is required')
    .min(2, 'Full name must be at least 2 characters')
    .max(100, 'Full name must be less than 100 characters'),
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),
  phone: z
    .string()
    .optional()
    .refine((val) => !val || /^\+?[\d\s-()]+$/.test(val), {
      message: 'Please enter a valid phone number',
    }),
  location: z
    .string()
    .optional(),
  dateOfBirth: z
    .string()
    .optional()
    .refine((val) => !val || new Date(val) <= new Date(), {
      message: 'Date of birth cannot be in the future',
    }),
  bio: z
    .string()
    .max(500, 'Bio must be less than 500 characters')
    .optional(),
  education: z
    .string()
    .max(200, 'Education must be less than 200 characters')
    .optional(),
  careerGoals: z
    .string()
    .max(1000, 'Career goals must be less than 1000 characters')
    .optional(),
  interests: z
    .array(z.string())
    .optional(),
  skills: z
    .array(z.string())
    .optional(),
});

// Settings schemas
export const passwordChangeSchema = z.object({
  current: z
    .string()
    .min(1, 'Current password is required'),
  new: z
    .string()
    .min(1, 'New password is required')
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'Password must contain at least one uppercase letter, one lowercase letter, and one number'),
  confirm: z
    .string()
    .min(1, 'Please confirm your new password'),
}).refine((data) => data.new === data.confirm, {
  message: "New passwords don't match",
  path: ["confirm"],
});

export const notificationSettingsSchema = z.object({
  email: z.boolean(),
  push: z.boolean(),
  sms: z.boolean(),
  deadlineReminders: z.boolean(),
  newOpportunities: z.boolean(),
  weeklyDigest: z.boolean(),
});

export const privacySettingsSchema = z.object({
  profileVisibility: z.enum(['public', 'private', 'connections']),
  showEmail: z.boolean(),
  showPhone: z.boolean(),
  dataSharing: z.boolean(),
});

export const preferencesSchema = z.object({
  theme: z.enum(['light', 'dark']),
  language: z.string(),
  timezone: z.string(),
  currency: z.string(),
});

// Timeline schemas
export const deadlineSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(100, 'Title must be less than 100 characters'),
  description: z
    .string()
    .max(500, 'Description must be less than 500 characters')
    .optional(),
  date: z
    .string()
    .min(1, 'Date is required')
    .refine((val) => new Date(val) > new Date(), {
      message: 'Deadline must be in the future',
    }),
  type: z.enum(['application', 'exam', 'interview', 'document', 'other']),
  priority: z.enum(['low', 'medium', 'high']),
  college: z
    .string()
    .optional(),
  course: z
    .string()
    .optional(),
  reminderDays: z
    .number()
    .min(0, 'Reminder days must be 0 or more')
    .max(365, 'Reminder days must be less than 365')
    .optional(),
});

// Search schemas
export const searchSchema = z.object({
  query: z
    .string()
    .min(1, 'Search query is required')
    .max(100, 'Search query must be less than 100 characters'),
  filters: z.object({}).optional(),
});

export const courseFiltersSchema = z.object({
  category: z.string().optional(),
  duration: z.string().optional(),
  level: z.string().optional(),
  mode: z.string().optional(),
  priceRange: z.object({
    min: z.number().min(0).optional(),
    max: z.number().min(0).optional(),
  }).optional(),
});

export const careerFiltersSchema = z.object({
  industry: z.string().optional(),
  experience: z.string().optional(),
  salaryRange: z.object({
    min: z.number().min(0).optional(),
    max: z.number().min(0).optional(),
  }).optional(),
  growth: z.string().optional(),
  location: z.string().optional(),
});

export const collegeFiltersSchema = z.object({
  type: z.string().optional(),
  location: z.string().optional(),
  ranking: z.object({
    min: z.number().min(1).optional(),
    max: z.number().min(1).optional(),
  }).optional(),
  fees: z.object({
    min: z.number().min(0).optional(),
    max: z.number().min(0).optional(),
  }).optional(),
  courses: z.array(z.string()).optional(),
});

// Assessment schemas
export const assessmentAnswerSchema = z.object({
  questionId: z.string(),
  answer: z.union([
    z.string(),
    z.number(),
    z.array(z.string()),
    z.boolean(),
  ]),
  timeSpent: z.number().min(0).optional(),
});

export const assessmentSubmissionSchema = z.object({
  assessmentId: z.string(),
  answers: z.array(assessmentAnswerSchema),
  totalTime: z.number().min(0),
  completedAt: z.string(),
});

// Contact form schema
export const contactSchema = z.object({
  name: z
    .string()
    .min(1, 'Name is required')
    .max(100, 'Name must be less than 100 characters'),
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),
  subject: z
    .string()
    .min(1, 'Subject is required')
    .max(200, 'Subject must be less than 200 characters'),
  message: z
    .string()
    .min(1, 'Message is required')
    .min(10, 'Message must be at least 10 characters')
    .max(1000, 'Message must be less than 1000 characters'),
});

// Export schema inference helpers (for JavaScript projects)
export const getLoginFormData = (data) => loginSchema.parse(data);
export const getRegisterFormData = (data) => registerSchema.parse(data);
export const getProfileFormData = (data) => profileSchema.parse(data);
export const getPasswordChangeFormData = (data) => passwordChangeSchema.parse(data);
export const getDeadlineFormData = (data) => deadlineSchema.parse(data);
export const getContactFormData = (data) => contactSchema.parse(data);
