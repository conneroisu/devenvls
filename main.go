package main

import (
	"context"
	"fmt"
	"os"
	"path/filepath"

	"github.com/alexaandru/go-sitter-forest/nix"
	sitter "github.com/alexaandru/go-tree-sitter-bare"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintf(os.Stderr, "Usage: %s <path-to-nix-file>\n", filepath.Base(os.Args[0]))
		os.Exit(1)
	}

	filePath := os.Args[1]
	content, err := os.ReadFile(filePath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
		os.Exit(1)
	}

	tree, err := sitter.Parse(
		context.TODO(),
		content,
		sitter.NewLanguage(nix.GetLanguage()),
	)
	if err != nil {
		panic(err)
	}

	// Print the syntax tree
	fmt.Println("Syntax Tree:")
	fmt.Printf("tree: %v\n", tree.Child(4).StartByte())
	fmt.Printf("root: %v\n", tree.Child(4).EndByte())
}
