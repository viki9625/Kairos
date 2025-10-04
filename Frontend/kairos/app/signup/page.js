// app/signup/page.js

import Link from 'next/link';

export default function SignupPage() {
  return (
    // Main container to center the form vertically and horizontally
    <div className="min-h-[84.5vh] bg-[#a7ebf2] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-[#023859] p-10 rounded-xl shadow-2xl">
        
        {/* Header */}
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-[#a7ebf2]">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-[#aff7ff]">
            Join our community and start your wellness journey.
          </p>
        </div>

        {/* Signup Form */}
        <form className="mt-8 space-y-6" action="#" method="POST">
          {/* Form Fields Container */}
          <div className="rounded-md shadow-sm space-y-4">
            
            {/* Name Field */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-[#a7ebf2]">
                Name
              </label>
              <input
                id="name"
                name="name"
                type="text"
                required
                placeholder="Enter your name"
                className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-[#91d7df] text-white rounded-md focus:outline-none focus:ring-blue-400 focus:border-blue-400 sm:text-sm"
              />
            </div>

            {/* Email Field */}
            <div>
              <label htmlFor="email-address" className="block text-sm font-medium text-[#a7ebf2]">
                Email
              </label>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                placeholder="Enter your email"
                className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-[#91d7df] text-white rounded-md focus:outline-none focus:ring-blue-400 focus:border-blue-400 sm:text-sm"
              />
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-[#a7ebf2]">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                placeholder="Enter your password"
                className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-[#91d7df] text-white rounded-md focus:outline-none focus:ring-blue-400 focus:border-blue-400 sm:text-sm"
              />
            </div>

            {/* Confirm Password Field */}
            <div>
              <label htmlFor="confirm-password" className="block text-sm font-medium text-[#a7ebf2]">
                Confirm Password
              </label>
              <input
                id="confirm-password"
                name="confirm-password"
                type="password"
                autoComplete="new-password"
                required
                placeholder="Confirm your password"
                className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-[#91d7df] text-white rounded-md focus:outline-none focus:ring-blue-400 focus:border-blue-400 sm:text-sm"
              />
            </div>
            
          </div>

          {/* Sign Up Button */}
          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-[#a7ebf2] bg-[#26658c] hover:bg-[#54acbf] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150"
            >
              Sign Up
            </button>
          </div>
        </form>
        
        {/* Log In Link */}
        <div className="text-center">
          <p className="text-sm text-[#91d7df]">
            Already have an account?{' '}
            <Link href="/login" className="font-medium text-[#a7ebf2] hover:underline">
              Log in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}