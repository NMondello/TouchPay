"use client";
import UserResponse from "@/components/userResponse/userResponse";
import { useSearchParams } from "next/navigation";

export default async function UserResponsePage() {

    const searchParams = useSearchParams();
    const mes = searchParams.get('message');
    let info = {name: "", email: "", provider: "", number: "", cvv: "", expiry: "",};

    if (mes) {
        const m = mes.split(" ");
        info['name'] = m[0];
        info['email'] = m[1];
        info['provider'] = m[2];
        info['number'] = m[3];
        info['cvv'] = m[4];
        info['expiry']= m[5];
    }

    return <UserResponse info={info}/>
}