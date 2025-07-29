import os
import shutil
import logging
import argparse
import face_recognition
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("image_sorter.log"),
        logging.StreamHandler()
    ]
)

def load_known_faces(known_dir):
    """
    Load known face encodings and names from directory
    
    Args:
        known_dir (str): Path to directory with subdirectories of known individuals
    
    Returns:
        tuple: (list of encodings, list of names)
    """
    known_encodings = []
    known_names = []
    
    # Iterate through each person's directory
    for person_name in os.listdir(known_dir):
        person_dir = os.path.join(known_dir, person_name)
        
        if not os.path.isdir(person_dir):
            continue
            
        logging.info(f"Loading images for {person_name}")
        
        # Process each image in the person's directory
        for img_file in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_file)
            
            # Skip non-image files
            if not img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            try:
                # Load image and get face encodings
                image = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(image)
                
                if len(encodings) > 0:
                    # Use the first face found in the image
                    known_encodings.append(encodings[0])
                    known_names.append(person_name)
                    logging.debug(f"  Loaded face from {img_file}")
                else:
                    logging.warning(f"  No faces found in {img_file}")
            except Exception as e:
                logging.error(f"  Error processing {img_file}: {str(e)}")
    
    return known_encodings, known_names

def process_images(source_dir, keep_dir, known_encodings, known_names, tolerance=0.6):
    """
    Process images from source directory and sort them
    
    Args:
        source_dir (str): Directory with images to process
        keep_dir (str): Directory to save images with recognized faces
        known_encodings (list): List of known face encodings
        known_names (list): List of names corresponding to encodings
        tolerance (float): Face recognition tolerance (lower is stricter)
    """
    # Create keep directory if it doesn't exist
    os.makedirs(keep_dir, exist_ok=True)
    
    # Get list of image files
    image_files = [f for f in os.listdir(source_dir) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        logging.warning("No images found in source directory")
        return
    
    logging.info(f"Found {len(image_files)} images to process")
    
    # Process each image
    for img_file in tqdm(image_files, desc="Processing images"):
        img_path = os.path.join(source_dir, img_file)
        keep = False
        recognized_names = []
        
        try:
            # Load image and detect faces
            image = face_recognition.load_image_file(img_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            # Check each face in the image
            for face_encoding in face_encodings:
                # Compare with known faces
                matches = face_recognition.compare_faces(
                    known_encodings, face_encoding, tolerance
                )
                
                # Check for any matches
                if True in matches:
                    keep = True
                    # Get names of recognized faces
                    matched_indices = [i for i, match in enumerate(matches) if match]
                    for idx in matched_indices:
                        recognized_names.append(known_names[idx])
        
            # Process based on recognition results
            if keep:
                # Move to keep folder
                dest_path = os.path.join(keep_dir, img_file)
                shutil.move(img_path, dest_path)
                names_str = ", ".join(set(recognized_names))
                logging.info(f"KEPT: {img_file} (Recognized: {names_str})")
            else:
                # Delete unrecognized image
                os.remove(img_path)
                logging.info(f"DELETED: {img_file} (No recognized faces)")
                
        except Exception as e:
            logging.error(f"ERROR processing {img_file}: {str(e)}")

def main():
    """Main function to handle command-line arguments and workflow"""
    parser = argparse.ArgumentParser(
        description="Sort images based on recognized faces"
    )
    parser.add_argument(
        "--source", 
        required=True,
        help="Directory containing images to sort"
    )
    parser.add_argument(
        "--keep", 
        required=True,
        help="Directory to save images with recognized faces"
    )
    parser.add_argument(
        "--known", 
        required=True,
        help="Directory with known individuals' images"
    )
    parser.add_argument(
        "--tolerance", 
        type=float,
        default=0.6,
        help="Face recognition tolerance (0.6 is default, lower is stricter)"
    )
    
    args = parser.parse_args()
    
    # Verify directories exist
    for dir_path in [args.source, args.known]:
        if not os.path.exists(dir_path):
            logging.error(f"Directory does not exist: {dir_path}")
            return
    
    logging.info("Loading known faces...")
    known_encodings, known_names = load_known_faces(args.known)
    
    if not known_encodings:
        logging.error("No valid face encodings loaded from known directory")
        return
    
    logging.info(f"Loaded {len(known_encodings)} face encodings")
    
    logging.info("Starting image processing...")
    process_images(
        source_dir=args.source,
        keep_dir=args.keep,
        known_encodings=known_encodings,
        known_names=known_names,
        tolerance=args.tolerance
    )
    logging.info("Processing complete!")

if __name__ == "__main__":
    main()