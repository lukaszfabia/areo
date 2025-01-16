import { Tokens, User, Weather } from "./models"
import { ACCESS_TOKEN } from "./token"

// DTO
type Model = string | User | Weather | Tokens

export interface Response<T extends Model> {
    status: "success" | "failed"
    data?: T | null
    error?: string | null
}



export interface Fetchable {
    method?: "POST" | "DELETE" | "GET" | "UPDATE"

    // form: {host}:{port} e.g endpoint /api/user/1
    endpoint: string

    token?: string | null;

    headers?: Record<string, string>;

    body?: any | null;
}

const host: string = process.env.HOST ?? `http://localhost:${process.env.APP_PORT}`


export const api = async <T extends Model>({
    method = "GET",
    endpoint,
    token = ACCESS_TOKEN,
    headers = {
        "content-type": "application/json;charset=UTF-8",
        ...(token && { Authorization: `Bearer ${token}` }),
    },
    body,
}: Fetchable): Promise<Response<T>> => {
    try {
        const url = `${host}${endpoint}`;

        const response = await fetch(url, {
            method,
            headers,
            body: body ? JSON.stringify(body) : undefined,
        });

        const json: Response<T> = await response.json();

        if (!response.ok) {
            return {
                error: json.error,
                status: "failed",
            }
        }

        return json;
    } catch (err) {
        console.log("API error: ", err)
        return {
            error: "Something went wrong!",
            status: "failed",
        }
    }
} 