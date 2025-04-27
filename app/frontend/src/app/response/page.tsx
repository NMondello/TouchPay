import Response from "@/components/formResponse/response";
import { useSearchParams } from "next/navigation";

export default async function ResponsePage() {

    const searchParams = useSearchParams();
    const mes = searchParams.get('message');
    let amount = null;
    if (mes) {
        amount = parseFloat(mes);
    }

    return <Response amount={amount}/>
}