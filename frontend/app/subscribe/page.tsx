'use client';

const SubscribePage = () => {
    const handleSubscribe = async () => {
        const res = await fetch('http://127.0.0.1:8000/api/subscriptions/create-checkout/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        });
        const data = await res.json();
        if (data.url) {
            window.location.href = data.url; // Redirect to Stripe Checkout
        } else {
            alert('Error creating checkout session');
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-2xl font-bold mb-4">Subscribe to Kickoff</h1>
            <button
                onClick={handleSubscribe}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
                Subscribe Now
            </button>
        </div>
    );
};

export default SubscribePage;
