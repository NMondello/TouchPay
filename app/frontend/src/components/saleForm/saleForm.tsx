"use client";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function saleForm() {

    const router = useRouter();

    const goToResponse = () => {
        router.push(`/saleResponse?message=${amount}`);
    }

    const [amount, setAmount] = useState(0);

    return (
        <div className = "flex items-center py-4">
            <Input
                placeholder="Enter amount"
                value={amount}
                onChange={(e) => setAmount(Number(e.target.value))}
             />
            <Button
                variant='ghost'
                onClick={goToResponse}
            >
                Receive Payment
            </Button>
        </div>
    )
}