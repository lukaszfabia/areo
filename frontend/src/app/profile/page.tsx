"use client";

import Loading from "@/components/ui/Spinner";
import { useAuth } from "@/providers/Auth";
import Login from "../login/page";
import { Weather } from "@/lib/models";
import { WeatherCard } from "@/components/WeatherCard"
import { WeatherList } from "@/components/WeatherList";


const current: Weather = {
    created_at: new Date(),
    updated_at: new Date(),
    temperature: 22,
    humidity: 23,
    pressure: 1023,
    altitude: 34,
    reader: "reader"
}


export default function Profile() {
    const { user, isLoading } = useAuth();

    if (!user) return <Login />
    if (isLoading) return <Loading />

    return (
        <section className="w-full p-20 space-y-10">
            <div className="flex w-1/3 text-center">
                <h1 className="lg:text-3xl md:text-2xl text-xl text-gray-500">Logged as <span className="mx-2 lg:text-5xl md:text-3xl text-2xl font-extrabold text-gray-50">{user.username ? user.username : user.email.split("@")}</span></h1>
            </div>
            <div className="flex gap-10">
                <WeatherCard weather={current} />

                <WeatherList />
            </div>

            <div className="flex gap-10">
                <div className="bg-gray-900 p-10 rounded-3xl shadow-xl w-fit space-y-10">
                    <h1 className="lg:text-4xl md:text-3xl text-2xl font-extrabold text-gray-100">Weather <span className="text-blue-500">Radar</span></h1>
                    <iframe width="1000" height="450" className="rounded-lg" src="https://embed.windy.com/embed2.html?lat=51&lon=17&detailLat=50.4&detailLon=17&width=1000&height=450&zoom=10&level=surface&overlay=wind&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"></iframe>
                </div>

                <div className="bg-gray-900 p-10 rounded-3xl shadow-xl w-fit space-y-10">
                    <h1 className="lg:text-4xl md:text-3xl text-2xl font-extrabold text-gray-100 text-right">User <span className="text-orange-500">Settings</span></h1>

                </div>
            </div>
        </section>
    )
}