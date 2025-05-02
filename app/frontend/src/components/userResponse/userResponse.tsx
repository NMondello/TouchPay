
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { Undo2 } from "lucide-react";
import { useEffect, useState } from 'react';

interface UserResponseProps {
    info : {
            name: string,
            email: string,
            provider: string,
            number: string,
            cvv: string,
            expiry: string
        }
}

export default function UserResponse({ info }: UserResponseProps) {
    const router = useRouter();

    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        const fetchData = async () => {
            let user = {};
            try {
                const res = await fetch('http://127.0.0.1:5002/add_user', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify(info),
                });
                if (!res.ok) {
                  console.log('Fetch failed with status:', res.status);
                } else {
                  user = await res.json();
                  console.log('Response data:', user);
                }
              } catch (err) {
                console.error('Error during fetch:', err);
              }
          setData(user);
          setLoading(false);
        };
    
        fetchData();
      }, [info]);
    
      if (loading) {
        return <div>Loading...</div>
      }
    

    const goToHome = () => {
        router.push(`/`);
    }


    return <div>
            {data['status'] ? 
                <div className="flex items-center py-4">
                    <h1>
                        {`User added successfully: ${data['message']}`}
                    </h1>
                    <Button variant='ghost' onClick={goToHome}>
                        <Undo2 />
                    </Button>
                </div>
            : 
                <div>
                    <h1>
                    {`User addition failed: ${data['message']}`}
                    </h1>
                    <Button variant='ghost' onClick={goToHome}>
                        <Undo2 />
                    </Button>
                </div>
            }
          </div>
}