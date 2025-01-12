"use client";

import { Features } from "@/components/Features";

export default function Home() {
  return (
    <main>
      <div className="bg-slate-950 min-h-screen text-white">
        <div className="flex flex-col items-center justify-center text-center py-20 bg-gradient-to-b from-slate-800 to-slate-950">
          <h1 className="text-4xl font-bold mb-4">
            Stay updated with <span className="bg-gradient-to-r from-pink-500 to-purple-500 text-transparent bg-clip-text">weather</span> and <span className="bg-gradient-to-r from-pink-500 to-purple-500 text-transparent bg-clip-text">air quality</span>!
          </h1>
          <p className="text-lg text-gray-300 mb-6">
            Personalized notifications, real-time monitoring, and full control – all in one place.
          </p>
          <button className="px-8 py-3 bg-gray-700 text-white font-bold rounded-lg shadow-lg hover:bg-gray-600">
            Join Now
          </button>
        </div>

        <div className="py-16 px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Our Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <Features />
          </div>
        </div>

        <div className="py-16 bg-slate-800 text-center">
          <h2 className="text-3xl font-bold mb-4">Join <span className="font-extrabold">Aero</span> today!</h2>
          <p className="text-gray-300 mb-6">Sign up and get started!</p>
          <button className="px-8 py-3 bg-gray-700 text-white font-bold rounded-lg shadow-lg hover:bg-gray-600">
            Sign Up
          </button>
        </div>
      </div>
    </main>
  );
}
