import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Bell, 
  Shield, 
  Palette, 
  Globe, 
  Download,
  Trash2,
  Eye,
  EyeOff,
  Save,
  Moon,
  Sun,
  Smartphone,
  Mail,
  MessageSquare,
  Heart,
  Plus,
  X
} from 'lucide-react';
import PageLayout from '../../components/layout/PageLayout';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { api } from '../../services/api';
import toast from 'react-hot-toast';

const Settings = () => {
  const [settings, setSettings] = useState({
    notifications: {
      email: true,
      push: true,
      sms: false,
      deadlineReminders: true,
      newOpportunities: true,
      weeklyDigest: false
    },
    privacy: {
      profileVisibility: 'public',
      showEmail: false,
      showPhone: false,
      dataSharing: true
    },
    preferences: {
      theme: 'light',
      language: 'en',
      timezone: 'Asia/Kolkata',
      currency: 'INR'
    }
  });

  const [showPassword, setShowPassword] = useState(false);
  const [passwords, setPasswords] = useState({
    current: '',
    new: '',
    confirm: ''
  });

  const [interests, setInterests] = useState([]);
  const [newInterest, setNewInterest] = useState('');
  const [isLoadingInterests, setIsLoadingInterests] = useState(false);

  // Predefined interest options
  const predefinedInterests = [
    'Data Science', 'Machine Learning', 'Web Development', 'Mobile Development',
    'Artificial Intelligence', 'Cybersecurity', 'Cloud Computing', 'DevOps',
    'UI/UX Design', 'Digital Marketing', 'Business Analytics', 'Finance',
    'Healthcare', 'Education', 'Engineering', 'Research', 'Entrepreneurship',
    'Project Management', 'Software Testing', 'Database Management'
  ];

  const handleSettingChange = (category, setting, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [setting]: value
      }
    }));
  };

  const handlePasswordChange = (field, value) => {
    setPasswords(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSaveSettings = () => {
    // Save settings logic here
    console.log('Settings saved:', settings);
  };

  const handleChangePassword = () => {
    // Change password logic here
    console.log('Password change requested');
  };

  const handleExportData = () => {
    // Export data logic here
    console.log('Data export requested');
  };

  const handleDeleteAccount = () => {
    // Delete account logic here
    console.log('Account deletion requested');
  };

  // Load user interests on component mount
  useEffect(() => {
    loadUserInterests();
  }, []);

  const loadUserInterests = async () => {
    try {
      setIsLoadingInterests(true);
      const response = await api.get('/users/me/interests');
      console.log('Interests API response:', response);
      
      // Handle different response structures
      let userInterests = [];
      if (response && response.interests) {
        userInterests = response.interests;
      } else if (response && response.data && response.data.interests) {
        userInterests = response.data.interests;
      } else if (Array.isArray(response)) {
        userInterests = response;
      }
      
      setInterests(userInterests || []);
      console.log('Loaded interests:', userInterests);
    } catch (error) {
      console.error('Failed to load interests:', error);
      console.error('Error details:', error.response || error);
      toast.error('Failed to load interests. Please try logging in again.');
    } finally {
      setIsLoadingInterests(false);
    }
  };

  const addInterest = (interest) => {
    if (interest && !interests.includes(interest)) {
      setInterests(prev => [...prev, interest]);
      setNewInterest('');
    }
  };

  const removeInterest = (interestToRemove) => {
    setInterests(prev => prev.filter(interest => interest !== interestToRemove));
  };

  const saveInterests = async () => {
    try {
      console.log('Saving interests:', interests);
      const response = await api.put('/users/me/interests', { interests });
      console.log('Save response:', response);
      toast.success('Interests updated successfully!');
      
      // Reload interests to ensure sync
      await loadUserInterests();
    } catch (error) {
      console.error('Failed to save interests:', error);
      console.error('Error details:', error.response || error);
      toast.error('Failed to save interests. Please try again.');
    }
  };

  const handleAddCustomInterest = () => {
    if (newInterest.trim()) {
      addInterest(newInterest.trim());
    }
  };

  return (
    <PageLayout title="Settings" subtitle="Manage your account preferences and privacy settings">
      <div className="max-w-4xl mx-auto space-y-6">
        
        {/* Notifications */}
        <Card>
          <Card.Header>
            <div className="flex items-center space-x-2">
              <Bell className="w-5 h-5 text-blue-600" />
              <Card.Title>Notifications</Card.Title>
            </div>
            <Card.Description>
              Choose how you want to be notified about updates and opportunities
            </Card.Description>
          </Card.Header>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Mail className="w-4 h-4 text-gray-500" />
                <div>
                  <p className="font-medium text-gray-900">Email Notifications</p>
                  <p className="text-sm text-gray-500">Receive updates via email</p>
                </div>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.notifications.email}
                  onChange={(e) => handleSettingChange('notifications', 'email', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Smartphone className="w-4 h-4 text-gray-500" />
                <div>
                  <p className="font-medium text-gray-900">Push Notifications</p>
                  <p className="text-sm text-gray-500">Receive push notifications on your device</p>
                </div>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.notifications.push}
                  onChange={(e) => handleSettingChange('notifications', 'push', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <MessageSquare className="w-4 h-4 text-gray-500" />
                <div>
                  <p className="font-medium text-gray-900">SMS Notifications</p>
                  <p className="text-sm text-gray-500">Receive important updates via SMS</p>
                </div>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.notifications.sms}
                  onChange={(e) => handleSettingChange('notifications', 'sms', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>

            <hr className="my-4" />

            <div className="space-y-3">
              <h4 className="font-medium text-gray-900">Notification Types</h4>
              
              {[
                { key: 'deadlineReminders', label: 'Deadline Reminders', desc: 'Get notified about upcoming application deadlines' },
                { key: 'newOpportunities', label: 'New Opportunities', desc: 'Discover new courses and career opportunities' },
                { key: 'weeklyDigest', label: 'Weekly Digest', desc: 'Weekly summary of your progress and recommendations' }
              ].map(({ key, label, desc }) => (
                <div key={key} className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-gray-900">{label}</p>
                    <p className="text-sm text-gray-500">{desc}</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={settings.notifications[key]}
                      onChange={(e) => handleSettingChange('notifications', key, e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              ))}
            </div>
          </div>
        </Card>

        {/* Privacy & Security */}
        <Card>
          <Card.Header>
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-green-600" />
              <Card.Title>Privacy & Security</Card.Title>
            </div>
            <Card.Description>
              Control your privacy settings and account security
            </Card.Description>
          </Card.Header>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Profile Visibility
              </label>
              <select
                value={settings.privacy.profileVisibility}
                onChange={(e) => handleSettingChange('privacy', 'profileVisibility', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="public">Public - Anyone can view your profile</option>
                <option value="private">Private - Only you can view your profile</option>
                <option value="connections">Connections - Only your connections can view</option>
              </select>
            </div>

            <div className="space-y-3">
              <h4 className="font-medium text-gray-900">Contact Information Visibility</h4>
              
              <div className="flex items-center justify-between">
                <span className="text-gray-700">Show email address</span>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.privacy.showEmail}
                    onChange={(e) => handleSettingChange('privacy', 'showEmail', e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-gray-700">Show phone number</span>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.privacy.showPhone}
                    onChange={(e) => handleSettingChange('privacy', 'showPhone', e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
            </div>

            <hr />

            <div>
              <h4 className="font-medium text-gray-900 mb-4">Change Password</h4>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Current Password
                  </label>
                  <div className="relative">
                    <input
                      type={showPassword ? "text" : "password"}
                      value={passwords.current}
                      onChange={(e) => handlePasswordChange('current', e.target.value)}
                      className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    >
                      {showPassword ? <EyeOff className="w-4 h-4 text-gray-400" /> : <Eye className="w-4 h-4 text-gray-400" />}
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    New Password
                  </label>
                  <input
                    type={showPassword ? "text" : "password"}
                    value={passwords.new}
                    onChange={(e) => handlePasswordChange('new', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Confirm New Password
                  </label>
                  <input
                    type={showPassword ? "text" : "password"}
                    value={passwords.confirm}
                    onChange={(e) => handlePasswordChange('confirm', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <Button onClick={handleChangePassword} className="w-full sm:w-auto">
                  Change Password
                </Button>
              </div>
            </div>
          </div>
        </Card>

        {/* Preferences */}
        <Card>
          <Card.Header>
            <div className="flex items-center space-x-2">
              <Palette className="w-5 h-5 text-purple-600" />
              <Card.Title>Preferences</Card.Title>
            </div>
            <Card.Description>
              Customize your app experience
            </Card.Description>
          </Card.Header>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Theme
              </label>
              <div className="flex items-center space-x-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="theme"
                    value="light"
                    checked={settings.preferences.theme === 'light'}
                    onChange={(e) => handleSettingChange('preferences', 'theme', e.target.value)}
                    className="mr-2"
                  />
                  <Sun className="w-4 h-4 mr-1" />
                  Light
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="theme"
                    value="dark"
                    checked={settings.preferences.theme === 'dark'}
                    onChange={(e) => handleSettingChange('preferences', 'theme', e.target.value)}
                    className="mr-2"
                  />
                  <Moon className="w-4 h-4 mr-1" />
                  Dark
                </label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Language
              </label>
              <select
                value={settings.preferences.language}
                onChange={(e) => handleSettingChange('preferences', 'language', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="bn">Bengali</option>
                <option value="te">Telugu</option>
                <option value="ta">Tamil</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Timezone
              </label>
              <select
                value={settings.preferences.timezone}
                onChange={(e) => handleSettingChange('preferences', 'timezone', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                <option value="Asia/Dubai">Asia/Dubai (GST)</option>
                <option value="Europe/London">Europe/London (GMT)</option>
                <option value="America/New_York">America/New_York (EST)</option>
              </select>
            </div>
          </div>
        </Card>

        {/* My Interests */}
        <Card>
          <Card.Header>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Heart className="w-5 h-5 text-pink-600" />
                <Card.Title>My Interests</Card.Title>
              </div>
              <button
                onClick={loadUserInterests}
                disabled={isLoadingInterests}
                className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors disabled:opacity-50"
              >
                {isLoadingInterests ? 'Loading...' : 'Refresh'}
              </button>
            </div>
            <Card.Description>
              Add your areas of interest to get personalized course recommendations
            </Card.Description>
          </Card.Header>

          <div className="space-y-4">
            {/* Current Interests */}
            <div>
              <h4 className="font-medium text-gray-900 mb-3">Your Interests</h4>
              {isLoadingInterests ? (
                <div className="flex items-center justify-center py-4">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                </div>
              ) : (
                <div className="flex flex-wrap gap-2 mb-4">
                  {interests.length === 0 ? (
                    <p className="text-gray-500 text-sm">No interests added yet. Add some to get personalized recommendations!</p>
                  ) : (
                    interests.map((interest, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.8 }}
                        className="flex items-center bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                      >
                        <span>{interest}</span>
                        <button
                          onClick={() => removeInterest(interest)}
                          className="ml-2 hover:bg-blue-200 rounded-full p-1 transition-colors"
                        >
                          <X className="w-3 h-3" />
                        </button>
                      </motion.div>
                    ))
                  )}
                </div>
              )}
            </div>

            {/* Add Custom Interest */}
            <div>
              <h4 className="font-medium text-gray-900 mb-3">Add Custom Interest</h4>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={newInterest}
                  onChange={(e) => setNewInterest(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAddCustomInterest()}
                  placeholder="Enter your interest..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <Button onClick={handleAddCustomInterest} className="flex items-center space-x-1">
                  <Plus className="w-4 h-4" />
                  <span>Add</span>
                </Button>
              </div>
            </div>

            {/* Predefined Interests */}
            <div>
              <h4 className="font-medium text-gray-900 mb-3">Popular Interests</h4>
              <div className="flex flex-wrap gap-2">
                {predefinedInterests
                  .filter(interest => !interests.includes(interest))
                  .map((interest, index) => (
                    <button
                      key={index}
                      onClick={() => addInterest(interest)}
                      className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-full text-sm transition-colors border border-gray-200 hover:border-gray-300"
                    >
                      {interest}
                    </button>
                  ))
                }
              </div>
            </div>

            {/* Save Interests Button */}
            <div className="pt-4 border-t">
              <Button onClick={saveInterests} className="flex items-center space-x-2">
                <Save className="w-4 h-4" />
                <span>Save Interests</span>
              </Button>
            </div>
          </div>
        </Card>

        {/* Data Management */}
        <Card>
          <Card.Header>
            <div className="flex items-center space-x-2">
              <Download className="w-5 h-5 text-orange-600" />
              <Card.Title>Data Management</Card.Title>
            </div>
            <Card.Description>
              Manage your data and account
            </Card.Description>
          </Card.Header>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
              <div>
                <h4 className="font-medium text-gray-900">Export Your Data</h4>
                <p className="text-sm text-gray-600">Download a copy of all your data</p>
              </div>
              <Button variant="outline" onClick={handleExportData} className="flex items-center space-x-2">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </Button>
            </div>

            <div className="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-200">
              <div>
                <h4 className="font-medium text-red-900">Delete Account</h4>
                <p className="text-sm text-red-600">Permanently delete your account and all data</p>
              </div>
              <Button variant="danger" onClick={handleDeleteAccount} className="flex items-center space-x-2">
                <Trash2 className="w-4 h-4" />
                <span>Delete</span>
              </Button>
            </div>
          </div>
        </Card>

        {/* Save Settings */}
        <div className="flex justify-end">
          <Button onClick={handleSaveSettings} className="flex items-center space-x-2">
            <Save className="w-4 h-4" />
            <span>Save All Settings</span>
          </Button>
        </div>
      </div>
    </PageLayout>
  );
};

export default Settings;
