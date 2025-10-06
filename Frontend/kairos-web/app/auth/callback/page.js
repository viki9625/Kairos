import { Suspense } from 'react';
import CallbackHandler from './CallbackHandler';

// A simple fallback component to show while the main component is loading in the browser.
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
            {/* Suspense tells Next.js to show the 'fallback' UI during the server build,
                and then render the full 'CallbackHandler' component in the user's browser.
                This prevents the build error related to useSearchParams. */}
            <Suspense fallback={<LoadingFallback />}>
                <CallbackHandler />
            </Suspense>
        </div>
    );
}

