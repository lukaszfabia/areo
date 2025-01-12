import { FC } from "react";
import "@fortawesome/react-fontawesome";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCloud } from "@fortawesome/free-solid-svg-icons";
import { Divider } from "@nextui-org/divider";
import Link from "next/link";

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

                <div className="space-y-2 md:space-y-4">
                    <h1 className="font-semibold text-lg md:text-xl">General</h1>
                    <ul className="text-gray-400 space-y-1">
                        <li>Element 1</li>
                        <li>Element 2</li>
                        <li>Element 3</li>
                    </ul>
                </div>

                <div className="space-y-2 md:space-y-4">
                    <h1 className="font-semibold text-lg md:text-xl">Follow Us</h1>
                    <ul className="text-gray-400 space-y-1">
                        <li>Element 1</li>
                        <li>Element 2</li>
                        <li>Element 3</li>
                    </ul>
                </div>
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
