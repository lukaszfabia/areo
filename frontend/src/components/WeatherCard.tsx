import { useEffect, useState } from "react";
import { Weather } from "@/lib/models";
import { transformTime } from "@/lib/time";
import { faCloud, faMountain, faTachometerAlt, faTint } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button } from "@heroui/react";
import Loading from "./ui/Spinner";
import { api } from "@/lib/api";

// const dummy: Weather = {
//     created_at: new Date(),
//     updated_at: new Date(),
//     temperature: 24.5,
//     humidity: 33.785221600087326,
//     pressure: 1001.2178316076133,
//     altitude: 100.6744304340726,
//     reader: "",
// }

export const WeatherCard = () => {
    const [weather, setWeather] = useState<Weather | null>(null);
    const [loading, setLoading] = useState(false);

    const fetchWeather = async () => {
        setLoading(true);
        try {
            const r = await api<Weather>({
                endpoint: "/weather/",
                apiVersion: "/api/v1",
            });

            setWeather(r.data ?? null);
        } catch (error) {
            console.error("Failed to fetch current data", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (!weather) {
            fetchWeather();
        }
    }, [weather]);

    if (loading || !weather) {
        return <Loading />;
    }

    return (
        <div className="bg-gray-900 p-6 md:p-10 rounded-3xl shadow-xl w-full max-w-md sm:max-w-lg lg:max-w-xl space-y-6 md:space-y-10">
            <div className="flex flex-col sm:flex-row items-center justify-between text-center sm:text-left mx-auto">
                <h1 className="font-extrabold text-gray-200 text-4xl sm:text-5xl md:text-6xl lg:text-7xl">
                    {weather.temperature?.toFixed(1)} &deg;C
                </h1>
                <FontAwesomeIcon icon={faCloud} className="text-5xl sm:text-6xl md:text-7xl my-4 text-gray-200" />
            </div>

            <div className="text-gray-300 space-y-4">
                <div className="flex items-center justify-center sm:justify-start text-lg">
                    <FontAwesomeIcon icon={faTint} className="mr-3 text-2xl sm:text-3xl text-gray-100" />
                    <p>
                        <span className="text-2xl sm:text-3xl text-gray-100">{weather.humidity?.toFixed(2)}</span> % Humidity
                    </p>
                </div>
                <div className="flex items-center justify-center sm:justify-start text-lg">
                    <FontAwesomeIcon icon={faTachometerAlt} className="mr-3 text-2xl sm:text-3xl text-gray-100" />
                    <p>
                        <span className="text-2xl sm:text-3xl text-gray-100">{weather.pressure?.toFixed(2)}</span> hPa Pressure
                    </p>
                </div>
                <div className="flex items-center justify-center sm:justify-start text-lg">
                    <FontAwesomeIcon icon={faMountain} className="mr-3 text-2xl sm:text-3xl text-gray-100" />
                    <p>
                        <span className="text-2xl sm:text-3xl text-gray-100">{weather.altitude?.toFixed(2)}</span> m Altitude
                    </p>
                </div>
            </div>

            <div className="text-gray-500 mt-4 text-center sm:text-left">
                <p className="text-sm">
                    Fetched at: <span className="text-gray-200">{transformTime(weather.created_at)}</span>
                </p>
            </div>

            <div className="flex items-center justify-center">
                <Button
                    color="secondary"
                    variant="shadow"
                    className="rounded-3xl"
                    onPress={fetchWeather}
                    isLoading={loading}
                >
                    What's the current???
                </Button>
            </div>
        </div>
    );
};
