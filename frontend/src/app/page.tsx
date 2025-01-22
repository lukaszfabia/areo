"use client";

import { Features } from "@/components/Features";
import Loading from "@/components/ui/Spinner";
import { useAuth } from "@/providers/Auth";
import { faArrowRight, faHeart } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, Snippet, Image } from "@heroui/react";

import Link from "next/link";

export default function Home() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <Loading />

  const getStartedPrompt = user ? "Go to Profile" : "Get Started"

  return (
    <main className="text-white">
      <section className="min-h-screen flex flex-col items-center justify-center text-center py-10 bg-gradient-to-b from-cyan-500 to-blue-900 relative">
        <div className="flex flex-col md:flex-row items-center gap-10 md:gap-20 lg:px-32 px-10 pt-10">
          <div className="md:w-1/2 text-left">
            <h1 className="lg:text-7xl md:text-5xl text-3xl font-bold mb-4">
              Stay updated with{" "}
              <span className="bg-gradient-to-r from-yellow-300 to-orange-500 text-transparent bg-clip-text font-rubik">
                weather
              </span>{" "}
              and{" "}
              <span className="bg-gradient-to-r from-green-400 to-teal-500 text-transparent bg-clip-text font-rubik">
                air quality
              </span>
              !
            </h1>
            <p className="text-lg text-gray-200 mb-6">
              Lorem ipsum dolor sit amet consectetur adipisicing elit.
              Distinctio nulla a dolores dicta accusamus et reprehenderit,
              doloremque at non quos similique, cupiditate labore repudiandae
              sequi soluta, qui placeat eveniet architecto.
            </p>
            <Button
              className="bg-gradient-to-tr from-pink-500 to-yellow-500 text-white shadow-lg"
              radius="full"
              size="lg"
              as={Link}
              href={user ? "/profile" : "/login"}
            >
              {getStartedPrompt}
              <FontAwesomeIcon icon={faArrowRight} className="w-4 h-4 md:w-5 md:h-5 ml-2" />
            </Button>
          </div>

          <div className="md:w-1/2 flex justify-center lg:pb-0 pb-20 max-sm:hidden">
            <Image
              alt="weather"
              height={600}
              src="/landingpage.svg"
              width={600}
              className="w-auto h-auto max-w-full"
            />
          </div>
        </div>
      </section>

      <div className="layer1 spacer"></div>

      <section className="pb-20 px-4 bg-white" id="features">
        <h2 className="lg:text-7xl md:text-5xl text-3xl font-bold text-center mb-10 text-black">
          Our <span className="text-blue-900">Features</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <Features />
        </div>
      </section>

      <div className="layer2 spacer"></div>

      <div className="spacer blob">
        <section className="bg-transparent text-center text-white py-28" id="docs">
          <h2 className="md:text-5xl text-3xl font-bold mb-4 text-green-400">
            Join to<span className="font-extrabold text-gray-100 font-playfair"> Aero</span> today!
          </h2>
          <div className="font-playfair text-gray-200 pb-4">
            {user ?
              <span>Thank you for choosing our product <FontAwesomeIcon icon={faHeart} className="text-pink-400" /></span>
              :
              <span>Sign up and get started!</span>
            }
          </div>
          <Button
            variant="ghost"
            radius="full"
            color="success"
            size="lg"
            as={Link}
            href={user ? "/profile" : "/login"}
          >
            {getStartedPrompt}
            <FontAwesomeIcon icon={faArrowRight} className="w-4 h-4 md:w-5 md:h-5 ml-2" />
          </Button>
        </section>
      </div >

      <div className="spacer layer5"></div>

      <section className="pb-10 bg-slate-950 text-center text-white lg:px-32 px-10" id="about">
        <h2 className="md:text-5xl text-3xl font-bold mb-4 text-gray-100 text-right">
          About <span className="font-extrabold text-fuchsia-500 font-playfair">project</span>
        </h2>

        <div className="flex flex-col md:flex-row  py-10">
          <div>
            <p className="text-left md:w-1/2">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Nostrum perspiciatis officiis sint voluptates recusandae doloribus. Quibusdam, rem nulla! Repellendus dolorem quasi expedita dolore exercitationem beatae fuga at praesentium explicabo minima.</p>
          </div>
          <div className="md:md-1/2 items-cener max-md:mt-10">
            <Snippet>docker-compose --env-file .env up --build -d</Snippet>
          </div>
        </div>
      </section>
    </main>
  );
}
