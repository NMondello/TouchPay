"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { Undo2 } from "lucide-react";

interface UserResponseProps {
    info: {[key: string]: string};
}

export default async function UserResponse({ info }: UserResponseProps) {
    const router = useRouter();

    const goToHome = () => {
        router.push(`/`);
    }

    const res = await fetch(`http://127.0.0.1:5002/add_user/${info}`, {
        cache: 'no-store',
      })

    const json = await res.json()

    return <div>
            {json['status'] ? 
                <div className="flex items-center py-4">
                    <h1>
                        {`User added successfully: ${json['message']}`}
                    </h1>
                    <Button variant='ghost' onClick={goToHome}>
                        <Undo2 />
                    </Button>
                </div>
            : 
                <div>
                    <h1>
                    {`User addition failed: ${json['message']}`}
                    </h1>
                    <Button variant='ghost' onClick={goToHome}>
                        <Undo2 />
                    </Button>
                </div>
            }
          </div>
}