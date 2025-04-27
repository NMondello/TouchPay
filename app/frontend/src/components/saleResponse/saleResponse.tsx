"use client";

import { TicketCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Undo2 } from "lucide-react";
import { useRouter } from "next/navigation";

interface SaleResponseProps {
    amount: number | null;
}
  
export default async function SaleResponse({ amount }: SaleResponseProps) {

    const router = useRouter();

    const goToHome = () => {
        router.push(`/`);
    }

    const res = await fetch(`http://127.0.0.1:5002/make_payment/${amount}`, {
        cache: 'no-store',
      })

    const json = await res.json()

    return (
        <div >
            {json['status'] ? 
                <div className="flex items-center py-4">
                    <h1>
                        {`Payment successful: ${json['message']}`}
                    </h1>
                    <TicketCheck className="text-green-500" />
                    <Button variant='ghost' onClick={goToHome}>
                        <Undo2 />
                    </Button>
                </div>
             : 
                <div>
                    <h1>
                    {`Payment failed: ${json['message']}`}
                    </h1>
                    <Button variant='ghost' onClick={goToHome}>
                        <Undo2 />
                    </Button>
                </div>
            }
        </div>
    );
}