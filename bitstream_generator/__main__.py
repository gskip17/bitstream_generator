import bitstream_generator
import sys
if __name__ == "__main__":
    print(sys.argv[1])
    if sys.argv[1] == "gui":
        import bitstream_generator.quickgen
    else:
        bitstream_generator.generate.main()
