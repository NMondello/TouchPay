"use client";

import { TicketCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Undo2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useState} from 'react';

interface SaleResponseProps {
    amount: number | null;
}
  
export default function SaleResponse({ amount }: SaleResponseProps) {

    const router = useRouter();

    const goToHome = () => {
        router.push(`/`);
    }

    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
        
    useEffect(() => {
    const fetchData = async () => {
        let payment = {};
        try {
            const res = await fetch(`http://127.0.0.1:5002/make_payment/${amount}`, {
                cache: 'no-store',
              });
            if (!res.ok) {
                console.log('Fetch failed with status:', res.status);
            } else {
                payment = await res.json();
                console.log('Response data:', payment);
            }
            } catch (err) {
            console.error('Error during fetch:', err);
            }
        setData(payment);
        setLoading(false);
    };

    fetchData();
    }, [amount]);

    if (loading) {
    return <div>Loading...</div>
    }

    return (
        <div >
            {data['status'] ? 
                <div className="flex items-center py-4">
                    <h1>
                        {`Payment successful: ${data['message']}`}
                    </h1>
                    <TicketCheck className="text-green-500" />
                    <Button variant='ghost' onClick={goToHome}>
                        <Undo2 />
                    </Button>
                </div>
             : 
                <div>
                    <h1>
                    {`Payment failed: ${data['message']}`}
                    </h1>
                    <Button variant='ghost' onClick={goToHome}>
                        <Undo2 />
                    </Button>
                </div>
            }
        </div>
    );
}