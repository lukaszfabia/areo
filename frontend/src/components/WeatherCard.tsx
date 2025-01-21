import { Weather } from "@/lib/models"
import { transformTime } from "@/lib/time";
import { faCloud, faMountain, faTachometerAlt, faTint } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"


export const WeatherCard = ({ weather }: { weather: Weather }) => {
    const { temperature, humidity, pressure, altitude, created_at, updated_at } = weather;

    return (
        <div className="bg-gray-900 p-10 rounded-3xl shadow-xl w-1/3 space-y-10">
            <div className="flex text-center justify-between items-center mx-10">
                <h1 className="font-extrabold text-gray-200 lg:text-8xl md:text-5xl text-3xl">{temperature} &deg; C</h1>
                <FontAwesomeIcon icon={faCloud} className="lg:text-8xl md:text-5xl text-3xl my-4" />
            </div>

            <div className="text-gray-300 my-2">
                <div className="flex items-center justify-center md:text-lg">
                    <FontAwesomeIcon icon={faTint} className="mr-2 md:text-3xl text-2xl text-gray-100" />
                    <p className="text-gray-300"><span className="md:text-3xl text-2xl text-gray-100">{humidity}</span> % Humidity</p>
                </div>
                <div className="flex items-center justify-center md:text-lg">
                    <FontAwesomeIcon icon={faTachometerAlt} className="mr-2 md:text-3xl text-2xl text-gray-100" />
                    <p className="text-gray-300"><span className="md:text-3xl text-2xl text-gray-100">{pressure}</span> hPa. Pressure</p>
                </div>
                <div className="flex items-center justify-center md:text-lg">
                    <FontAwesomeIcon icon={faMountain} className="mr-2 md:text-3xl text-2xl text-gray-100" />
                    <p className="text-gray-300"><span className="md:text-3xl text-2xl text-gray-100">{altitude}</span> m. Altitude</p>
                </div>
            </div>

            <div className="text-gray-500 mt-4">
                <p className="text-sm">Fetched at: <span className="text-gray-200">{transformTime(created_at)}</span></p>
            </div>
        </div>
    );
};