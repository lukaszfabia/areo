export const meta = {
    title: 'Aero',
    desc: 'Check and collect weather conditions'
}

export const themes = {
    dark: "dark",
    light: "light",
}


export interface Link {
    text: string,
    dest: string,
}


export const menu: Link[] = [
    { text: "Feautres", dest: "#features" },
    { text: "Docs", dest: "#docs" },
    { text: "About", dest: "#about" },
    { text: "Login", dest: "/login" }
]


export const socials: Link[] = [
    { text: "github.com/areo", dest: "https://github.com/lukaszfabia/areo" },
    { text: "Lukasz Fabia", dest: "https://lukaszfabia.vercel.app" },
    { text: "Piotr Ryszko", dest: "https://github.com/rychu777" }
]

export const general: Link[] = menu


export const passwordRegex: RegExp = new RegExp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")