import { motion } from "framer-motion";
import { usePathname, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

const LoadingScreen = () => {
  const [isNavigating, setIsNavigating] = useState(false);
  const pathname = usePathname();
  const searchParams = useSearchParams();
  useEffect(() => {
    setIsNavigating(false);
  }, [pathname, searchParams]);

  if (!isNavigating) {
    return null;
  }
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-white">
      <div className="relative">
        {/* Background pulse effect */}
        <motion.div
          className="absolute inset-0 bg-gray-100 rounded-full -z-10"
          initial={{ scale: 0.9 }}
          animate={{ scale: 1.2 }}
          transition={{
            type: "spring",
            stiffness: 260,
            damping: 20,
            repeat: Infinity,
            repeatType: "reverse",
            duration: 1.5,
          }}
        ></motion.div>

        {/* Text Animation */}
        <motion.div
          initial={{ y: -20 }}
          animate={{ y: 0 }}
          transition={{
            type: "spring",
            stiffness: 300,
            damping: 15,
            repeat: Infinity,
            repeatType: "reverse",
            duration: 1.5,
          }}
          className="px-8 py-4"
        >
          <h1 className="text-4xl font-bold text-gray-800">Parfumelier</h1>
        </motion.div>
      </div>
    </div>
  );
};

export default LoadingScreen;
