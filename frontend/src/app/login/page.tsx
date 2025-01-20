"use client";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, Link } from "@nextui-org/react";
import { GenericForm as Form } from "@/components/Form";
import { AuthProps, useAuth } from "@/providers/Auth";
import Loading from "@/components/ui/Spinner";
import Profile from "../profile/page";
import { FormEvent, useRef } from "react";



export default function Login() {
    const { user, auth, isLoading, error } = useAuth();
    const ref = useRef<HTMLInputElement>(null);


    const submit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const form = new FormData(e.currentTarget)

        const body: AuthProps = {
            password: form.get("password")!.toString(),
            email: form.get("email")!.toString(),
            on_create: false,
            remember_me: ref.current?.checked ?? false,
        }


        auth(body)
    }

    if (user) return <Profile />
    if (isLoading) return <Loading />

    return (
        <section>
            <div className="text-center space-y-2">  <h1 className="lg:text-5xl md:text-3xl text-xl font-extrabold">Hello Again!</h1>
                <p className="text-gray-500">You've been missed!</p>
                {error && <p className="text-red-600">{error}</p>}
            </div>
            <Form
                refOnRememberMe={ref}
                className="pt-5"
                onSubmit={submit}
            >
                <div className="space-y-5 w-full">
                    <div className="flex justify-between">
                        <Link href="sign-up" size="sm">Forgot password?</Link>
                        <Link href="sign-up" size="sm">Don't have an account?</Link>
                    </div>


                    <div className="w-full flex flex-col">
                        <Button
                            type="submit"
                            className="bg-gradient-to-tr from-blue-500 to-cyan-400 text-white hover:scale-105 transform transition-transform"
                        >
                            {isLoading ? <Loading /> :
                                <>Login
                                    <FontAwesomeIcon icon={faArrowRight} className="w-4 h-4 md:w-5 md:h-5 ml-2" />
                                </>
                            }
                        </Button>
                    </div>
                </div>
            </Form>
        </section>
    );
}
