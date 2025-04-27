"use client";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function UserForm() {

    const router = useRouter();

    const goToResponse = () => {
        const m = [name, email, provider, number, cvv, expiry];
        const mes = m.join(" ");
        router.push(`/userResponse?message=${mes}`);
    }

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [provider, setProvider] = useState("");
    const [number, setNumber] = useState("");
    const [cvv, setCvv] = useState("");
    const [expiry, setExpiry] = useState("");

    return (
        <div>
            <div className = "flex items-center py-4">
                <Input
                    placeholder="Enter name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
            </div>
            <div className = "flex items-center py-4">
                <Input
                    placeholder="Enter email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>
            <div className = "flex items-center py-4">
                <Input
                    placeholder="Enter credit card provider"
                    value={provider}
                    onChange={(e) => setProvider(e.target.value)}
                />
            </div>
            <div className = "flex items-center py-4">
                <Input
                    placeholder="Enter credit card number"
                    value={number}
                    onChange={(e) => setNumber(e.target.value)}
                />
            </div>
            <div className = "flex items-center py-4">
                <Input
                    placeholder="Enter CVV"
                    value={cvv}
                    onChange={(e) => setCvv(e.target.value)}
                />
            </div>
            <div className = "flex items-center py-4">
                <Input
                    placeholder="Enter card expiry date"
                    value={expiry}
                    onChange={(e) => setExpiry(e.target.value)}
                />
            </div>
            <Button
                variant='ghost'
                onClick={goToResponse}
            >
                Add Fingerprint
            </Button>
        </div>
    )
}