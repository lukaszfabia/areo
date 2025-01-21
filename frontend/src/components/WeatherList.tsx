import { Table, TableHeader, TableColumn, TableBody, Spinner, TableRow, TableCell, getKeyValue } from "@heroui/react";
import React from "react";
import { useAsyncList } from "@react-stately/data";
import { Weather } from "@/lib/models";


const weatherData: Weather[] = [
    {
        _id: "23adfv23",
        created_at: new Date("2025-01-01T12:00:00Z"),
        updated_at: new Date("2025-01-01T14:00:00Z"),
        temperature: 22,
        humidity: 60,
        pressure: 1013,
        altitude: 150,
        reader: "Sensor A"
    },
    {
        _id: "2323",
        created_at: new Date("2025-01-02T12:00:00Z"),
        updated_at: new Date("2025-01-02T14:00:00Z"),
        temperature: 19,
        humidity: 65,
        pressure: 1010,
        altitude: 200,
        reader: "Sensor B"
    },
    {
        _id: "2334er23",
        created_at: new Date("2025-01-03T12:00:00Z"),
        updated_at: new Date("2025-01-03T14:00:00Z"),
        temperature: 25,
        humidity: 55,
        pressure: 1015,
        altitude: 100,
        reader: "Sensor C"
    },
    {
        _id: "232dfg3",
        created_at: new Date("2025-01-04T12:00:00Z"),
        updated_at: new Date("2025-01-04T14:00:00Z"),
        temperature: 20,
        humidity: 70,
        pressure: 1020,
        altitude: 50,
        reader: "Sensor D"
    }
];

export const WeatherList = () => {
    const [isLoading, setIsLoading] = React.useState(false);

    let list = useAsyncList<Weather, string>({
        async load({ }) {
            return {
                items: [...weatherData],
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
                                    {getKeyValue(item, columnKey)}
                                </TableCell>
                            )}
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    );
};