import { Card, CardHeader, CardBody } from "@heroui/react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChartLine, faCloudSunRain, faWalking, IconDefinition } from "@fortawesome/free-solid-svg-icons";

export interface Feature {
    header: string,
    desc: string,
    icon: IconDefinition,
}


export const features: Feature[] = [
    {
        header: "Real-time Weather Monitoring",
        desc: "Track current weather conditions and air quality live from your devices.",
        icon: faCloudSunRain,
    },
    {
        header: "Activity Recommendations",
        desc: "Get suggestions for outdoor and indoor activities based on current weather.",
        icon: faWalking,
    },
    {
        header: "Historical Data Analysis",
        desc: "Access and analyze past weather and air quality data to identify trends.",
        icon: faChartLine,
    }, {
        header: "Easy dashboard",
        desc: "Manage read station from local webiste",
        icon: faCloudSunRain,
    },
    {
        header: "Log by via RFID Card",
        desc: "Get suggestions for outdoor and indoor activities based on current weather.",
        icon: faWalking,
    },
    {
        header: "Persnonalize your data",
        desc: "Just choose what weather data you want to focus on!",
        icon: faChartLine,
    },

];


export const Features = () => {
    return (
        <>
            {features.map((feature: Feature, index: number) => (
                <Card className="py-4 bg-gray-100 shadow-lg" key={`${feature.header} ${index}`}>
                    <CardHeader className="pb-0 pt-2 px-4 flex-col items-start">
                        <div className="flex items-center gap-2">
                            <div className="w-12 h-12 relative flex justify-center p-3 rounded-full items-center bg-slate-200 text-gray-700 hover:scale-110 transition-transform duration-300">
                                <div className="absolute inset-0 rounded-full bg-slate-200 opacity-40 blur-lg"></div>
                                <FontAwesomeIcon icon={feature.icon} className="text-xl z-10 text-secondary-500" />
                            </div>
                            <h4 className="font-bold text-md text-default-300">{feature.header}</h4>
                        </div>
                        <small className="text-default-500 pt-4">{feature.desc}</small>
                    </CardHeader>
                    <CardBody className="overflow-visible py-2">
                        {/* <Image
                            alt="Card background"
                        /> */}
                    </CardBody>
                </Card>
            ))}
        </>
    )
}