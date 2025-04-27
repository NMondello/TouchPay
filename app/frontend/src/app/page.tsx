"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export default function Home() {

  const router = useRouter();

  const goToPaymentForm = () => {
    router.push(`/saleForm`);
  }

  const goToUserForm = () => {
    router.push(`/userForm`);
  }

  return <div className="flex items-center py-4">
          <div className = "flex items-center py-4">
            <Button
                variant='ghost'
                onClick={goToPaymentForm}
            >
              Make a Sale
            </Button>
          </div>
          <div className = "flex items-center py-4">
            <Button
                variant='ghost'
                onClick={goToUserForm}
            >
              Add Fingerprint
            </Button>
          </div>
         </div>
}
