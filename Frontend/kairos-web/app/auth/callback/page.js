import { Suspense } from 'react';
import CallbackHandler from './CallbackHandler';

// A simple fallback component to show while the client-side component is loading.
const LoadingFallback = () => (
    <div className="text-center">
        <p className="text-xl font-semibold text-[#023859]">
            Loading...
        </p>
    </div>
);

export default function AuthCallbackPage() {
    return (
        <div className="min-h-[84.5vh] bg-[#a7ebf2] flex items-center justify-center">
            {/* Suspense tells Next.js to show the 'fallback' UI on the server,
                and then render the 'CallbackHandler' component in the browser.
                This prevents the build error. */}
            <Suspense fallback={<LoadingFallback />}>
                <CallbackHandler />
            </Suspense>
        </div>
    );
}
