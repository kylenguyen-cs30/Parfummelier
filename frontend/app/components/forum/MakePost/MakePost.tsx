import React, { useState } from "react";
import Image from "next/image";
import Dialog from "@/app/components/ui/dialog/diaglog";
import Textarea from "@/app/components/ui/textarea/textarea";
import Input from "@/app/components/ui/input/input";
import Button from "../../ui/button/Button";
import { X } from "lucide-react";

const MakePostModal = ({ isOpen, onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    title: "",
    content: "",
    topic: "",
    image_urls: [],
  });
  const [images, setImages] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleImageChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    const files = Array.from(e.target.files);
    setIsLoading(true);

    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      const response = await fetch(
        "http://localhost:8000/posts/upload-images",
        {
          method: "POST",
          body: formData,
        },
      );
      const data = await response.json();
      setFormData((prev) => ({
        ...prev,
        image_urls: [...prev.image_urls, ...data.image_urls],
      }));
      setImages((prev) => [...prev, ...files]);
    } catch (error) {
      console.error("Error Uploading Images: ", error);
    } finally {
      setIsLoading(false);
    }
  };

  //NOTE: Handle submit the form
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await onSubmit(formData);
      setFormData({ title: "", content: "", topic: "", image_urls: [] });
      setImages([]);
      onClose();
    } catch (error) {
      console.error("error creating post:", error);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
        <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold">Create New Post</h2>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-6 w-6" />
            </Button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Title</label>
              <Input
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                required
                className="w-full"
                placeholder="Enter post title"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Topic</label>
              <Input
                name="topic"
                value={formData.topic}
                onChange={handleInputChange}
                required
                className="w-full"
                placeholder="Enter post topic"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Content</label>
              <Textarea
                name="content"
                value={formData.content}
                onChange={handleInputChange}
                required
                className="w-full min-h-[200px]"
                placeholder="Write your post content here..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Images</label>
              <Input
                type="file"
                multiple
                accept="image/*"
                onChange={handleImageChange}
                className="w-full"
              />
              {images.length > 0 && (
                <div className="mt-2 flex gap-2 flex-wrap">
                  {images.map((image, index) => (
                    <div key={index} className="relative">
                      <Image
                        src={URL.createObjectURL(image)}
                        alt={`Preview ${index + 1}`}
                        fill
                        className="object-cover rounded"
                        sizes="80px"
                      />
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? "Creating..." : "Create Post"}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </Dialog>
  );
};

export default MakePostModal;
