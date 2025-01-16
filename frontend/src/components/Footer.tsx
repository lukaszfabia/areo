'use client';

import { FC } from "react";
import "@fortawesome/react-fontawesome";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCloud } from "@fortawesome/free-solid-svg-icons";
import { Divider } from "@nextui-org/divider";
import { Link } from "@nextui-org/react";
import { general, Link as lnk, socials } from "@/lib/config";

const Links: FC<{ collection: lnk[], title: string, mustBeExternal?: boolean }> = ({ collection, title, mustBeExternal = false }) => {
    return (
        <div className="space-y-2 md:space-y-4">
            <h1 className="font-semibold text-lg md:text-xl">{title}</h1>
            <ul className="text-gray-400 space-y-1">
                {collection.map((lnk: lnk, index: number) => (
                    <li key={`${lnk.text}-${index}`}>
                        <Link href={lnk.dest} color="foreground" isExternal showAnchorIcon={mustBeExternal}>{lnk.text}</Link>
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
                            <span className="font-semibold">weather conditions</span>{" "}
                            with <Link href="https://www.raspberrypi.com/" isExternal showAnchorIcon>RaspberryPi</Link>
                        </p>
                    </div>
                </div>
                <Links title="General" collection={general} />
                <Links title="Follow Us" collection={socials} mustBeExternal />
            </div>

            <Divider className="my-4" />

            <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0 text-gray-400 text-sm md:text-base">
                <p>&copy; 2024 Aero, Inc. All rights reserved.</p>
                <div className="flex space-x-6">
                    <Link href={"#"}>
                        Terms & Conditions
                    </Link>
                    <Link href={"#"}>
                        Privacy Policy
                    </Link>
                </div>
            </div>
        </footer >
    );
};
