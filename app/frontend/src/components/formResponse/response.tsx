"use client";

import { TicketCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Undo2 } from "lucide-react";
import { useRouter } from "next/navigation";

interface ResponseProps {
    amount: number | null;
}
  
export default async function Response({ amount }: ResponseProps) {
    const status = true;

    const router = useRouter();

    const goToForm = () => {
        router.back()
    }

    const res = await fetch(`http://127.0.0.1:5002/make_payment/${amount}`, {
        cache: 'no-store',
      })

    const json = await res.json()

    return (
        <div >
            {status ? 
                <div className="flex items-center py-4">
                    <h1>
                        {`Payment Successful in the amount of ${amount}`}
                    </h1>
                    <TicketCheck className="text-green-500" />
                    <Button onClick={goToForm}>
                        <Undo2 />
                    </Button>
                </div>
             : 
                <div>
                    <h1>
                        {`Payment Failed`}
                    </h1>
                </div>
            }
        </div>
    );
}