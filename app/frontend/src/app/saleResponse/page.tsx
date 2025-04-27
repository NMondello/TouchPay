import SaleResponse from "@/components/saleResponse/saleResponse";
import { useSearchParams } from "next/navigation";

export default async function SaleResponsePage() {

    const searchParams = useSearchParams();
    const mes = searchParams.get('message');
    let amount = null;
    if (mes) {
        amount = parseFloat(mes);
    }

    return <SaleResponse amount={amount}/>
}