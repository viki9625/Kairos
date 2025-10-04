// app/page.js

import Link from "next/link";

export default function WelcomePage() {
  return (
    <>
      <div className="bg-[#a7ebf2] min-h-[84.5vh] flex flex-col items-center justify-center text-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-8">
          <h1 className="text-5xl font-bold text-[#011c40]">
            Your Personal Wellness Companion
          </h1>
          <p className="text-lg px-4 sm:px-0 text-gray-700">
            Begin your journey to a healthier, happier you. Kairos offers
            personalized support for both your mental and physical well-being.
          </p>

          <div className="flex gap-4 justify-center">
            <Link href={"/signup"}>
              <button className="bg-[#26658c] text-[#a7ebf2] px-5 py-2 rounded-full font-semibold">
                <span>Sign Up Now</span>
              </button>
            </Link>
            <Link href={"/login"}>
              <button className="bg-[#54acbf] px-5 py-2 rounded-full font-semibold">
                <span>Log In</span>
              </button>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
