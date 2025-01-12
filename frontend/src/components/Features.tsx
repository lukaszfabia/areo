import { Card, CardHeader, CardBody, Image } from "@nextui-org/react";
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
    },

];


export const Features = () => {
    return (
        <>
            {features.map((feature: Feature, index: number) => (
                <Card className="py-4 bg-slate-900 border border-slate-950 shadow-lg" key={`${feature.header} ${index}`}>
                    <CardHeader className="pb-0 pt-2 px-4 flex-col items-start">
                        <div className="flex items-center gap-2">
                            <div className="w-12 h-12 relative flex justify-center p-3 rounded-full items-center bg-slate-800 text-gray-300 shadow-md hover:scale-110 transition-transform duration-300">
                                <div className="absolute inset-0 rounded-full bg-slate-700 opacity-40 blur-lg"></div>
                                <FontAwesomeIcon icon={feature.icon} className="text-xl z-10 text-secondary-500" />
                            </div>
                            <h4 className="font-bold text-md">{feature.header}</h4>
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