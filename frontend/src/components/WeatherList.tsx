import { Table, TableHeader, TableColumn, TableBody, Spinner, TableRow, TableCell, getKeyValue } from "@heroui/react";
import React, { Key } from "react";
import { useAsyncList } from "@react-stately/data";
import { Weather, WeatherPaginated } from "@/lib/models";
import { api } from "@/lib/api";


const formatValue = (columnName: Key, value: string | number | Date) => {
    if (columnName === "created_at") {
        return new Date(value).toLocaleString("pl-PL", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    } else if (typeof value === "number") {
        return value.toFixed(2);
    }
    return value;
};

export const WeatherList = () => {
    const [isLoading, setIsLoading] = React.useState(false);

    let list = useAsyncList<Weather, string>({
        async load({ }) {
            setIsLoading(true)

            let items: Weather[] = [];

            try {
                const res = await api<WeatherPaginated>({
                    apiVersion: "/api/v1",
                    endpoint: "/weather-history/",
                })

                console.log(res)

                if (res.data) {
                    console.log(res.data.data)

                    const weather = res.data.data as Weather[]

                    items = weather
                }
            } catch (error) {
                console.log("Something went wrong")
            }

            setIsLoading(false)
            return {
                items: items,
            };
        },
        async sort({ items, sortDescriptor }) {
            return {
                items: items.sort((a, b) => {
                    const first = a[sortDescriptor.column as keyof Weather];
                    const second = b[sortDescriptor.column as keyof Weather];
                    let cmp = 0;

                    if (typeof first === 'number' && typeof second === 'number') {
                        cmp = first - second;
                    } else if (first instanceof Date && second instanceof Date) {
                        cmp = first.getTime() - second.getTime();
                    } else {
                        const firstValue = first !== null ? (typeof first === 'string' ? first : String(first)) : '';
                        const secondValue = second !== null ? (typeof second === 'string' ? second : String(second)) : '';

                        cmp = firstValue.localeCompare(secondValue);
                    }

                    if (sortDescriptor.direction === 'descending') {
                        cmp *= -1;
                    }

                    return cmp;
                }),
            };
        },
    });


    return (
        <div className="bg-gray-900 p-10 rounded-3xl shadow-xl w-2/3 space-y-4">
            <h1 className="lg:text-4xl md:text-3xl text-2xl font-extrabold text-gray-100">Historical <span className="text-green-600">Weather</span> Data</h1>
            <Table
                aria-label="Weather table with client side sorting"
                classNames={{
                    wrapper: "bg-slate-900",
                    tbody: "bg-slate-900",
                    th: "bg-gray-700",
                }}
                sortDescriptor={list.sortDescriptor}
                onSortChange={list.sort}
            >
                <TableHeader>
                    <TableColumn key="temperature" allowsSorting>
                        Temperature (°C)
                    </TableColumn>
                    <TableColumn key="humidity" allowsSorting>
                        Humidity (%)
                    </TableColumn>
                    <TableColumn key="pressure" allowsSorting>
                        Pressure (hPa)
                    </TableColumn>
                    <TableColumn key="altitude" allowsSorting>
                        Altitude (m)
                    </TableColumn>
                    <TableColumn key="created_at">
                        Read at
                    </TableColumn>
                </TableHeader>
                <TableBody
                    isLoading={isLoading}
                    items={list.items}
                    loadingContent={<Spinner label="Loading..." />}
                >
                    {(item: Weather) => (
                        <TableRow key={item._id?.toString()} className="hover:bg-slate-800 transition-all duration-200 cursor-pointer">
                            {(columnKey) => (
                                <TableCell className="px-6 py-4 text-gray-300">
                                    {`${formatValue(columnKey, getKeyValue(item, columnKey))}`}
                                </TableCell>
                            )}
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    );
};