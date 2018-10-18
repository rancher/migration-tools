package cmd

import (
	"io"
	"os"
)

func SaveFile(file string, content []byte) error {
	f, err := os.Create(file)
	if err != nil {
		return err
	}
	defer f.Close()

	_, err = f.Write(content)
	if err != nil {
		return err
	}

	return nil
}

func IsDirEmpty(name string) (bool, error) {
	f, err := os.Open(name)
	if os.IsNotExist(err) {
		return true, nil
	}
	if err != nil {
		return false, err
	}
	defer f.Close()

	// read in ONLY one file
	_, err = f.Readdir(1)

	// and if the file is EOF... well, the dir is empty.
	if err == io.EOF {
		return true, nil
	}

	return false, err
}

func CreateDir(path string) error {
	_, err := os.Stat(path)

	if os.IsNotExist(err) {
		return os.MkdirAll(path, 0755)
	}

	return err
}
