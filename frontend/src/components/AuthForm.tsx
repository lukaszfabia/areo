import { useAuth, AuthProps } from "@/providers/Auth";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, Link } from "@heroui/react";
import { FC, FormEvent, useRef } from "react";
import Loading from "./ui/Spinner";
import { GenericForm as Form } from "./Form";
import { redirect } from "next/navigation";


// literals
const textPrimary = (login: boolean) => login ? "Hello Again!" : "Welcome!"
const textSecondary = (login: boolean) => login ? "You've been missed!" : "We're glad that you have chosen us."
const buttonText = (login: boolean) => login ? "Login" : "Sign Up"


export const AuthForm: FC<{ login?: boolean }> = ({ login = false }) => {
    const { user, auth, isLoading, error } = useAuth();
    const ref = useRef<HTMLInputElement>(null);


    const submit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const form = new FormData(e.currentTarget)

        const body: AuthProps = {
            password: form.get("password")!.toString(),
            email: form.get("email")!.toString(),
            on_create: !login,
            remember_me: ref.current?.checked ?? false,
        }


        auth(body)
    }

    if (user) {
        redirect("/profile")
    }

    if (isLoading) return <Loading />

    return (
        <section>
            <div className="text-center space-y-2">  <h1 className="lg:text-5xl md:text-3xl text-xl font-extrabold">{textPrimary(login)}</h1>
                <p className="text-gray-500">{textSecondary(login)}</p>
                {error && <p className="text-red-600">{error}</p>}
            </div>
            <Form
                refOnRememberMe={ref}
                className="pt-5"
                onSubmit={submit}
            >
                <div className="space-y-5 w-full">
                    <div className="flex justify-between">
                        {/* sign up */}
                        {!login && <Link href="/login" size="sm">Already have account?</Link>}
                        {/* login */}
                        {login &&
                            <>
                                <Link href="/rfid-auth" size="sm">Auth without passes?</Link>
                                <Link href="/sign-up" size="sm">Don't have an account?</Link>
                            </>
                        }
                    </div>


                    <div className="w-full flex flex-col">
                        <Button
                            type="submit"
                            className="bg-gradient-to-tr from-blue-500 to-cyan-400 text-white hover:scale-105 transform transition-transform"
                        >
                            {isLoading ? <Loading /> :
                                <>{buttonText(login)}
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
