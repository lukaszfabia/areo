import { FC } from "react";
import "@fortawesome/react-fontawesome";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCloud } from "@fortawesome/free-solid-svg-icons";
import { Divider } from "@nextui-org/divider";
import Link from "next/link";
import { general, Link as lnk, socials } from "@/lib/config";

const Links: FC<{ collection: lnk[], title: string }> = ({ collection, title }) => {
    return (
        <div className="space-y-2 md:space-y-4">
            <h1 className="font-semibold text-lg md:text-xl">{title}</h1>
            <ul className="text-gray-400 space-y-1">
                {collection.map((lnk: lnk, index: number) => (
                    <li key={`${lnk.text}-${index}`}>
                        <Link href={lnk.dest} target="_blank">{lnk.text}</Link>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export const Footer: FC = () => {
    return (
        <footer className="p-6 md:p-12 bg-slate-950 text-white">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-5 space-y-6 md:space-y-0">
                <div className="space-y-3 md:space-y-5">
                    <div className="font-bold font-rubik text-2xl md:text-3xl">
                        Aero
                    </div>
                    <div className="flex items-center text-sm md:text-base">
                        <p>
                            Check and collect{" "}
                            <span className="font-semibold">weather conditions</span>
                        </p>
                        <FontAwesomeIcon icon={faCloud} className="w-4 h-4 md:w-5 md:h-5 ml-2" />
                    </div>
                </div>
                <Links title="General" collection={general} />
                <Links title="Follow Us" collection={socials} />
            </div>

            <Divider className="my-4" />

            <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0 text-gray-400 text-sm md:text-base">
                <p>&copy; 2024 Aero, Inc. All rights reserved.</p>
                <div className="flex space-x-6">
                    <Link href={"#"} className="hover:text-white">
                        Terms & Conditions
                    </Link>
                    <Link href={"#"} className="hover:text-white">
                        Privacy Policy
                    </Link>
                </div>
            </div>
        </footer>
    );
};
