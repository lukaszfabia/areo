import { Tokens, User, Weather, WeatherPaginated } from "./models"
import getToken, { ACCESS } from "./token"

type FailedRequest = {
    detail: string
}

// DTO
type Model = User | Weather | Tokens | WeatherPaginated

export interface Response<T extends Model> {
    data?: T | null
    detail?: string | null
}



export interface Fetchable {
    method?: "POST" | "DELETE" | "GET" | "PUT"

    apiVersion?: "/api/v1" | "/api/v2"

    // provide endpoint like /sign-in/
    endpoint: string

    token?: string | null;

    headers?: Record<string, string>;

    body?: Record<string, any> | null;
}

// const host: string = `http://${process.env.API_HOST}:${process.env.API_PORT}`
const host: string = "http://0.0.0.0:8000"


export const api = async <T extends Model>({
    method = "GET",
    apiVersion = "/api/v1",
    endpoint,
    token = getToken(ACCESS),
    headers = {
        "content-type": "application/json;charset=UTF-8",
        ...(token && { Authorization: `Bearer ${token}` }),
    },
    body,
}: Fetchable): Promise<Response<T>> => {
    try {
        const url = `${host}${apiVersion}${endpoint}`;

        const response = await fetch(url, {
            method,
            headers,
            body: body ? JSON.stringify(body) : undefined,
        });


        if (response.ok) {
            const data: T = await response.json()
            const result: Response<T> = {
                data: data
            }
            return result
        }

        const data: FailedRequest = await response.json()
        const result: Response<T> = {
            detail: data.detail
        }
        return result

    } catch (err) {
        console.log("API error: ", err)
        return {
            detail: "Something went wrong!",
        }
    }
} 