# Extension file
OUTPUT = anki_liberator.ankiaddon 

# Files to include in the extension
FILES = config.md config.json __init__.py README.md

# Target to create the zip archive
publish:
	@echo "Creating $(OUTPUT)..."
	zip $(OUTPUT) $(FILES)
	@echo "$(OUTPUT) created successfully."

# Clean up the generated zip file
clean:
	@echo "Cleaning up..."
	rm -f $(OUTPUT)
	@echo "Clean up completed."

repackage: clean publish
