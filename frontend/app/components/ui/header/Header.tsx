import Image from "next/image";

const Header = () => {
  return (
    <header className="bg-gray-800 text-white p-4 flex justify-center items-center relative">
      <span className="text-2xl font-bold">Parfummelier</span>

      {/* Right side: Profile Button */}
      <div className="absolute right-4 flex items-center">
        <button className="bg-gray-700 p-2 rounded-full focus:outline-none">
          <Image
            src="/logo/Logo.webp"
            alt="Profile"
            width={32} // Adjust width here for profile image
            height={32} // Adjust height here for profile image
            className="rounded-full"
          />
        </button>
      </div>
    </header>
  );
};

export default Header;
