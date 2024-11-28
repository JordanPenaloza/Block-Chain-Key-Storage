from seal import *

def generate_and_print_public_key():
    # Set encryption parameters
    parms = EncryptionParameters(scheme_type.bgv)
    poly_modulus_degree = 1024
    parms.set_poly_modulus_degree(poly_modulus_degree)
    parms.set_coeff_modulus(CoeffModulus.BFVDefault(poly_modulus_degree))
    parms.set_plain_modulus(PlainModulus.Batching(poly_modulus_degree, 20))

    # Create SEALContext
    context = SEALContext(parms)

    # Generate keys
    keygen = KeyGenerator(context)
    public_key = keygen.create_public_key()

    # Save public key to a file
    public_key_file = "public_key.seal"
    public_key.save(public_key_file)

    # Read and print the serialized public key
    with open(public_key_file, "rb") as f:
        public_key_data = f.read()
        print("Public Key Serialized:")
        print(public_key_data.hex())  # Convert to hexadecimal for display

if __name__ == "__main__":
    generate_and_print_public_key()
