// app/about/page.js

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-[#a7ebf2] flex flex-col items-center py-4 sm:py-8 md:py-12 px-2 sm:px-4 md:px-6">
      <div className="w-full max-w-4xl mx-auto space-y-6 sm:space-y-8 md:space-y-12">
        
        {/* Section: About Kairos */}
        <section className="space-y-3 sm:space-y-4">
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-[#011c40] leading-tight">
            About Kairos: Seizing the Moment for Your Mental Well-being
          </h1>
          <p className="mt-2 sm:mt-4 text-sm sm:text-base md:text-lg text-gray-600">
            Welcome to Kairos, your confidential and compassionate space for mental wellness.
          </p>
          <p className="text-sm sm:text-base md:text-lg text-gray-700 leading-relaxed">
            In Greek, Kairos means "the opportune moment"—the right time for meaningful change. We chose this name because we believe that now is the time to prioritize your mental health, overcome the hesitation that comes with stigma, and take the first brave step toward accessing the support you deserve.
          </p>
        </section>

        {/* Section: Our Mission */}
        <section className="space-y-3 sm:space-y-4 pt-4 sm:pt-6 md:pt-8">
          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-[#011c40] leading-snug">
            Our Mission: Breaking Down Barriers, Building Up Hope
          </h2>
          <div className="space-y-3 sm:space-y-4">
            <p className="text-sm sm:text-base md:text-lg text-gray-700 leading-relaxed">
              We know that for many young people, asking for help can feel overwhelming. The fear of being judged or misunderstood—the reality of stigma—often stands as a silent barrier.
            </p>
            <p className="text-sm sm:text-base md:text-lg text-gray-700 leading-relaxed">
              Our mission is simple: To provide a safe, private, and empathetic path for youth to explore their feelings, learn coping skills, and confidently access the help they need, all without fear of judgment.
            </p>
          </div>
        </section>

        {/* Features Grid - Modified for better mobile display */}
        <section className="space-y-3 sm:space-y-4 pt-4 sm:pt-6 md:pt-8">
          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-[#011c40] leading-snug">
            How Kairos Works: Confidentiality Meets Compassion
          </h2>
          <p className="text-sm sm:text-base md:text-lg text-gray-700 leading-relaxed">
            Kairos is more than just an app; it's a trusted companion built on cutting-edge, yet profoundly human, principles.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 mt-4 sm:mt-6">
            {/* Feature Cards with improved mobile spacing */}
            <div className="bg-white/80 backdrop-blur-sm rounded-lg p-4 sm:p-6 shadow-md sm:shadow-lg">
              <h3 className="text-lg sm:text-xl md:text-2xl font-semibold text-gray-800 mb-2 sm:mb-4">
                Powered by Empathy
              </h3>
              <p className="text-sm sm:text-base text-gray-700 leading-relaxed">
                At the heart of Kairos is our proprietary AI model, designed with a deep understanding of youth psychology and communication. It provides empathetic, non-judgmental support that listens actively and guides gently.
              </p>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-lg p-4 sm:p-6 shadow-md sm:shadow-lg">
              <h3 className="text-lg sm:text-xl md:text-2xl font-semibold text-gray-800 mb-2 sm:mb-4">
                Commitment to Confidentiality
              </h3>
              <p className="text-sm sm:text-base text-gray-700 leading-relaxed">
                Your privacy is our highest priority. Kairos is 100% confidential. There are no report cards, no notifications sent to parents or schools, and no social pressure.
              </p>
            </div>
          </div>

          {/* Bridge to Real Help - Improved mobile layout */}
          <div className="bg-white/80 backdrop-blur-sm rounded-lg p-4 sm:p-6 shadow-md sm:shadow-lg mt-4 sm:mt-6">
            <h3 className="text-lg sm:text-xl md:text-2xl font-semibold text-gray-800 mb-2 sm:mb-4">
              A Bridge to Real Help
            </h3>
            <p className="text-sm sm:text-base text-gray-700 leading-relaxed mb-3 sm:mb-4">
              We are here to do more than just listen. Kairos acts as a guided pathway. As you engage with the platform, the AI can help you:
            </p>
            <ul className="list-disc list-inside text-sm sm:text-base text-gray-700 space-y-2">
              <li className="transition-transform hover:translate-x-2 duration-200">
                Identify and understand your emotions
              </li>
              <li className="transition-transform hover:translate-x-2 duration-200">
                Develop healthy coping mechanisms and resilience skills
              </li>
              <li className="transition-transform hover:translate-x-2 duration-200">
                Confidently explore and access professional mental health resources
              </li>
            </ul>
          </div>
        </section>

        {/* Join Movement - Better mobile optimization */}
        <section className="space-y-3 sm:space-y-4 pt-4 sm:pt-6 md:pt-8 text-center">
          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-[#011c40] leading-snug">
            Join the Movement
          </h2>
          <p className="text-sm sm:text-base md:text-lg text-gray-700 leading-relaxed">
            We believe that seeking support is a sign of incredible strength, not weakness. Kairos is here to affirm that strength.
          </p>
          <p className="text-base sm:text-lg md:text-xl font-bold text-gray-800">
            This is your opportune moment. This is your Kairos.
          </p>
        </section>
      </div>
    </div>
  );
}