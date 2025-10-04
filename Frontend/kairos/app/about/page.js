// app/about/page.js

export default function AboutPage() {
  return (
    // Main container to center content, similar to the welcome page
    <div className="min-h-screen bg-[#a7ebf2] flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl w-full space-y-12 text-center">
        
        {/* Section: About Kairos */}
        <section className="space-y-4">
          <h1 className="text-4xl sm:text-5xl font-extrabold text-[#011c40] leading-tight">
            About Kairos: Seizing the Moment for Your Mental Well-being
          </h1>
          <p className="mt-4 text-lg sm:text-xl text-gray-600 px-4 sm:px-0">
            Welcome to Kairos, your confidential and compassionate space for mental wellness.
          </p>
          <p className="text-lg text-gray-700 leading-relaxed px-4 sm:px-0">
            In Greek, Kairos means "the opportune moment"—the right time for meaningful change. We chose this name because we believe that now is the time to prioritize your mental health, overcome the hesitation that comes with stigma, and take the first brave step toward accessing the support you deserve.
          </p>
        </section>

        {/* Section: Our Mission */}
        <section className="space-y-4 pt-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-[#011c40] leading-snug">
            Our Mission: Breaking Down Barriers, Building Up Hope
          </h2>
          <p className="text-lg text-gray-700 leading-relaxed px-4 sm:px-0">
            We know that for many young people, asking for help can feel overwhelming. The fear of being judged or misunderstood—the reality of stigma—often stands as a silent barrier.
          </p>
          <p className="text-lg text-gray-700 leading-relaxed px-4 sm:px-0">
            Our mission is simple: To provide a safe, private, and empathetic path for youth to explore their feelings, learn coping skills, and confidently access the help they need, all without fear of judgment.
          </p>
        </section>

        {/* Section: How Kairos Works */}
        <section className="space-y-4 pt-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-[#011c40] leading-snug">
            How Kairos Works: Confidentiality Meets Compassion
          </h2>
          <p className="text-lg text-gray-700 leading-relaxed px-4 sm:px-0">
            Kairos is more than just an app; it’s a trusted companion built on cutting-edge, yet profoundly human, principles.
          </p>

          {/* Subsection: Powered by Empathy */}
          <div className="text-left space-y-2 max-w-2xl mx-auto pt-4">
            <h3 className="text-2xl font-semibold text-gray-800">Powered by Empathy</h3>
            <p className="text-base text-gray-700 leading-relaxed">
              At the heart of Kairos is our proprietary AI model, designed with a deep understanding of youth psychology and communication. It provides empathetic, non-judgmental support that listens actively and guides gently, offering personalized tools and strategies tailored to your unique emotional landscape.
            </p>
          </div>

          {/* Subsection: Commitment to Confidentiality */}
          <div className="text-left space-y-2 max-w-2xl mx-auto pt-4">
            <h3 className="text-2xl font-semibold text-gray-800">Commitment to Confidentiality</h3>
            <p className="text-base text-gray-700 leading-relaxed">
              Your privacy is our highest priority. Kairos is 100% confidential. There are no report cards, no notifications sent to parents or schools, and no social pressure. This is your space to be honest, vulnerable, and real. You are in control of your journey, and your interactions remain secure and private.
            </p>
          </div>

          {/* Subsection: A Bridge to Real Help */}
          <div className="text-left space-y-2 max-w-2xl mx-auto pt-4">
            <h3 className="text-2xl font-semibold text-gray-800">A Bridge to Real Help</h3>
            <p className="text-base text-gray-700 leading-relaxed">
              We are here to do more than just listen. Kairos acts as a guided pathway. As you engage with the platform, the AI can help you:
            </p>
            <ul className="list-disc list-inside text-base text-gray-700 pl-4 space-y-1">
              <li>Identify and understand your emotions.</li>
              <li>Develop healthy coping mechanisms and resilience skills.</li>
              <li>Confidently explore and access professional mental health resources in your area, when you are ready.</li>
            </ul>
          </div>
        </section>

        {/* Section: Join the Movement */}
        <section className="space-y-4 pt-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-[#011c40] leading-snug">
            Join the Movement
          </h2>
          <p className="text-lg text-gray-700 leading-relaxed px-4 sm:px-0">
            We believe that seeking support is a sign of incredible strength, not weakness. Kairos is here to affirm that strength.
          </p>
          <p className="text-xl font-bold text-gray-800 px-4 sm:px-0">
            This is your opportune moment. This is your Kairos.
          </p>
        </section>

      </div>
    </div>
  );
}