"use client";

import Loading from "@/components/ui/Spinner";
import { useAuth } from "@/providers/Auth";
import Login from "../login/page";
import { User } from "@/lib/models";
import { WeatherCard } from "@/components/WeatherCard"
import { WeatherList } from "@/components/WeatherList";
import { Button, Chip, cn, Form, Input, Spinner, Switch, TimeInput } from "@heroui/react";
import { FormEvent, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMobile, faPlus } from "@fortawesome/free-solid-svg-icons";
import { EmailUpdate } from "@/components/ui/Email";
import { PasswordUpdate } from "@/components/ui/Password";
import { UsernameUpdate } from "@/components/ui/Username";
import { Time, toTime } from "@internationalized/date";


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
                <WeatherCard />

                <WeatherList />
            </div>

            <div className="flex gap-10">
                {/* <div className="bg-gray-900 p-10 rounded-3xl shadow-xl w-fit space-y-10">
                    <h1 className="lg:text-4xl md:text-3xl text-2xl font-extrabold text-gray-100">Weather <span className="text-blue-500">Radar</span></h1>
                    <iframe width="600" height="450" className="rounded-lg" src="https://embed.windy.com/embed2.html?lat=51&lon=17&detailLat=50.4&detailLon=17&width=1000&height=450&zoom=10&level=surface&overlay=wind&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"></iframe>
                </div> */}
                <Settings user={user!} />
            </div>
        </section>
    )
}

// TODO: refactor
function Settings({ user }: { user: User }) {
    const { isLoading, update, addRfid } = useAuth();
    const [enabledNotifications, setEnabledNotifications] = useState(user.settings?.notifications ?? false);
    const [notifyByEmail, setNotifyByEmail] = useState(user.settings?.notify_by_email ?? false);
    // make request to firebase 
    const [newTime, setNewTime] = useState<Time | null>(null);
    const [error, setError] = useState<string | null>(null);


    const handleToken = () => { };

    const [times, setTimes] = useState<Time[]>(user.settings?.times?.map((e: any) => toTime(e)) ?? []);

    const handleClose = (timeToRemove: Time) => {
        setTimes(times.filter((e) => e !== timeToRemove));
    };

    const handleAddTime = () => {
        if (newTime && !times.some((e) => e.toString() === newTime.toString()) && times.length < 6) {
            setTimes((prevTimes) => [...prevTimes, newTime]);
            setNewTime(null);
        }
    };

    const submit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        setError(null);
        const form = new FormData(e.currentTarget)

        const body: Record<string, any> = {}

        form.forEach((value, key) => {
            if (value.toString().length > 0) {
                body[key] = value
            }
        })

        body.settings = body.settings || {}

        if (times.length > 0) {
            body.settings.times = times
        }

        body.settings.notify_by_email = notifyByEmail
        body.settings.notifications = enabledNotifications

        console.log(body)

        update(body)
    }


    return (
        <div className="bg-gray-900 p-10 rounded-3xl shadow-xl w-full space-y-8">
            <h1 className="lg:text-4xl md:text-3xl text-2xl font-extrabold text-gray-100">
                User <span className="text-orange-500">Settings</span>
            </h1>
            {error && <p className="text-red-500">{error}</p>}

            <div className="flex flex-wrap space-y-8 md:space-y-0 md:space-x-4 w-full">
                <section className="bg-gray-800 p-5 rounded-2xl flex-1 space-y-5">
                    <h1 className="lg:text-xl md:text-lg font-extrabold">Notifications</h1>
                    <p className="text-gray-300">Choose a way to get notified about current weather.</p>

                    <Form className="py-5 space-y-4 w-full" id="notifications-form" onSubmit={submit}>
                        <Switch
                            isSelected={notifyByEmail}
                            onValueChange={setNotifyByEmail}
                            classNames={{
                                base: cn(
                                    "inline-flex flex-row-reverse w-full max-w-md items-center",
                                    "justify-between cursor-pointer rounded-lg gap-1 p-4 border-2 border-transparent"
                                ),
                                wrapper: "p-0 h-4 overflow-visible",
                                thumb: cn(
                                    "w-6 h-6 border-2 shadow-lg",
                                    "group-data-[hover=true]:border-primary",
                                    "group-data-[selected=true]:ms-6",
                                    "group-data-[pressed=true]:w-7",
                                    "group-data-[selected]:group-data-[pressed]:ms-4"
                                ),
                            }}
                        >
                            <div className="flex flex-col gap-1">
                                <p className="text-medium">Email notifications</p>
                                <p className="text-tiny text-default-400">
                                    Get notifications on your device or email.
                                </p>
                            </div>
                        </Switch>

                        <Switch
                            isSelected={enabledNotifications}
                            onValueChange={setEnabledNotifications}
                            classNames={{
                                base: cn(
                                    "inline-flex flex-row-reverse w-full max-w-md items-center",
                                    "justify-between cursor-pointer rounded-lg gap-1 p-4 border-2 border-transparent"
                                ),
                                wrapper: "p-0 h-4 overflow-visible",
                                thumb: cn(
                                    "w-6 h-6 border-2 shadow-lg",
                                    "group-data-[hover=true]:border-primary",
                                    "group-data-[selected=true]:ms-6",
                                    "group-data-[pressed=true]:w-7",
                                    "group-data-[selected]:group-data-[pressed]:ms-4"
                                ),
                            }}
                        >
                            <div className="flex flex-col gap-1">
                                <p className="text-medium">Device notifications</p>
                                <p className="text-tiny text-default-400">
                                    Get notifications on your device or email.
                                </p>
                            </div>
                        </Switch>

                        <p className="text-gray-300">To be notified on your phone, just click the button below.</p>
                        <div className="flex items-center justify-between space-x-6 w-full">
                            <Input
                                isReadOnly
                                className="w-full"
                                defaultValue={user.settings?.rfid_uid ?? "XXX-XXX-XXX"}
                                label="Device Token"
                                type="text"
                                variant="bordered"
                            />
                            <Button variant="ghost" size="lg" onPress={addRfid}>
                                <span>Add rfid</span>
                                <FontAwesomeIcon icon={faMobile} />
                            </Button>
                        </div>
                    </Form>
                </section>

                <section className="bg-gray-800 p-5 rounded-2xl flex-1 space-y-5">
                    <h1 className="lg:text-xl md:text-lg font-extrabold">Account</h1>
                    <p className="text-gray-300">Update your data and settings (e.g., read time).</p>

                    <Form className="py-5 space-y-4 w-full" id="account-form" onSubmit={submit} autoComplete="off">
                        <EmailUpdate defaultValue={user.email} />

                        <PasswordUpdate />

                        <UsernameUpdate defaultValue={user.username ?? ""} />

                        <p className="text-gray-300">Your read times.</p>
                        <div className="flex gap-3">
                            <div className="flex gap-5 items-center">
                                <TimeInput
                                    value={newTime}
                                    onChange={setNewTime}
                                    label="Read time"
                                    className="w-fit"
                                    variant="bordered"

                                />
                                <Button
                                    onPress={handleAddTime}
                                    isIconOnly
                                    variant="shadow"
                                    color="success"
                                    size="sm"
                                    radius="full"
                                    startContent={<FontAwesomeIcon icon={faPlus} />}
                                />
                            </div>

                            <div className="flex flex-wrap gap-2">
                                {times.map((time: Time, index: number) => (
                                    <Chip
                                        key={index}
                                        variant="flat"
                                        className="gap-2 m-1"
                                        onClose={() => handleClose(time)}
                                    >
                                        {time.toString()}
                                    </Chip>
                                ))}
                            </div>
                        </div>

                    </Form>
                </section>
            </div>

            <div className="flex justify-end gap-3">
                <Button type="reset" color="default" variant="flat" form="account-form">
                    Reset
                </Button>
                <Button type="submit" color="success" variant="ghost" form="account-form">
                    {isLoading ? <Spinner size="sm" color="white" /> : <>Save</>}
                </Button>
            </div>
        </div>

    )
}