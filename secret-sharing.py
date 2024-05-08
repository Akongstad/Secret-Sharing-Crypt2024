#File is written for Python 3
#The code uses matplotlib library for plotting the shares as points, so make sure to have it installed.
#To run the code, use cli and type: "python3 .\secret-sharing.py"
#The code is tested and are assumed to be working as expected.
#See comments in the code for more information.
#The file opens with constants and field operations, then the split_secret function, reconstruct function and test function.

import secrets
import matplotlib.pyplot as plt

# CONSTS
F_HEX = "0x00b44a0bc6303782b729a7f9b44a3611b247ddf1e544f8b1420e2aae976003219175461d2bd76e64ba657d7c9dff6ed7b17980778ec0cbf75fc16e52463e2d784f5f20c1691f17cdc597d7a5141080809a38c635b2a62082e310aa963ca15953894221ad54c6b30aea10f4dd88a66c55ab9c413eae49c0b28e6a3981e0021a7dcb0759af34b095ce3efce78938f2a2bed70939ba47591b88f908db1eadf237a7a7100ac87130b6119d7ae41b35fd27ff6021ac928273c20f0b3a01df1e6a070b8e2e93b5220ad02104000c0c1e82e17fd00f6ac16ef37c3b6153d348e470843a84f25473a51f040a42671cd94ffc989eb27fd42b817f8173bfa95bdfa17a2ae22fd5c89dab2822bcc973b5b90f8fadc9b074cca8f9365b1e8994ff0bda48b1f7498cce02d4e794915f8a4208de3eaf9fbff5"
F = int(F_HEX, 16)

SHARE_1 = int(
    "009aca2ca92b1e95bfad348c9014c6adc00d18d29fd5f891d0837c9fe18db35cc28d654114d6159dd6664405ead5277e24bcdbda9984c28e3b810377744f420e0fc52ada1cafb328f6aaa9656d31c73b98af938f784d3d611e7e6f124119e948745d15c829d794f47eb76b3fdfc16824ff6d46bcf534b1a2d8b3f2de97250f3f3b16f87dba41d54b127c10b2b44d7d54c00d89ce91b590c065cc210dd841c8460a7ac535fb0a6e26b312695c2635b5a8d311fb4473bee791f35f92dc70524954f5f60b98352e4d63b1f8c7357c1e52d696f67b2ff14a988a1691352fa0d3401d7d4f806598b651e5e21bc133ad2340a327cef3d47ef2bddc386a98dabcebaa814becb09ce3d8032d933664af6b495849030b03e6da89d971e5a45f19ecdef254e3549ba5af53ed18b7a013c81b154a06eb76",
    16)
SHARE_2 = int(
    "2131de2d5f973cd76289fe88dfe2cd9e8196b7cfb26b8793fb3afa5bc0b965441878cf300f1a39db3525dc4881a4b4654bf648b6b812e202d0ea3e7654fe02cadc68f72978093eee3731ecd0ff1f7b32e52de1d9e7575315112cbe693205a0890ae8a2fe33610e9097ce3c7f819113315686179c226df4bea68cca4e466fcf4ca343fa60019ca4914acedc84df0e12c8ad4a3d5590f51e321a7f3528dfb7939241e1377c632e913813ac02757d899a19c10900fdd4ed24d1affc0249b3fdd93df4de4f229dffa039af1589f5fe87cf7594cc8379f364a64334ecc165aa650cf81edc2fd1791b95128926c9be25b94e60fad290d3f5ef79403025d2ead3ae2f77cc054f4dbc3a5183d31eeb8626c00512769ad03092f0b2f256fc2b2f8b6250659e656c1569d96b164d7e0908f84e99e728",
    16)
SHARE_4 = int(
    "71da02f27e8f8f82fc996469dc254f81b4db7718ca8bc4fe86f6700424c9527db41c2403b69ea80fb2902fa720983929691c81b88a7c5bf830b5153d749327b9a80422f2a61cd51b5c5c7568a059ab38660f135e05ba62a5e6014d3f0ce4b0522b81df3231b111c06199faa7cff0387981dd35cc62ea6a451d2c0b12b39f6676adbe82058c3cb4847856477f8f93962c4c10fc5fb62906d95bcb7aad486b564d8c3f50cbeb2d21b6aa0e8e46d03b9ba75b1adf4fa9d41ca32e977fbdafadaa4f38f20020d30c5f26e30ac1ad56993bc246c06fd0bcbb12e540b1fa6292ba403f45f03f9cf446ac4a37bb4aa180a3f262466d3129fccca216c1521143cabc818dda793ce26b3b700c3b15cd648193771e797863f7782e6b460d593c92b15a90c843d9d09f65ff1b25cda9b758baa456fe15",
    16)

# N = 5, k = 3
SHARES = [(1, SHARE_1), (2, SHARE_2), (4, SHARE_4)]


# Field operations (to be used in conjunction with pow() for exponentiation)
def F_add(a, b, F=F) -> int:
    """
    Add two numbers in the field.
    :param a: First number.
    :param b: Second number.
    :return: a + b.
    """
    return (a + b) % F


def F_sub(a, b, F=F) -> int:
    """
    Subtract two numbers in the field.
    :param a: First number.
    :param b: Second number.
    :return: a - b.
    """
    return (a - b) % F


def F_mul(a, b, F=F) -> int:
    """
    Multiply two numbers in the field.
    :param a: First number.
    :param b: Second number.
    :return: a * b.
    """
    return (a * b) % F


def F_div(a, b, F=F) -> int:
    """
    Divide two numbers in the field.
    :param a: First number.
    :param b: Second number.
    :return: a / b.
    """
    return F_mul(a, pow(b, -1, F))


def sample_coefficients(k, F=F) -> []:
    """sample k coefficients from F. (Use secrets for cryptographically secure random numbers.)"""
    for i in range(k):
        yield secrets.randbelow(F)  # Q: Can these be < 0?


def split_secret(S, N, k, F=F) -> []:
    """
    Split the secret S into N shares with the polynomial definition from the lecture
    :param N: # of shares to split into.
    :param k: # shares for reconstruction. deg(f) = k - 1.
    :return: List of N shares with k needed for reconstruction. Share: (i, f(i)).
    """
    as_ = [S] + list(sample_coefficients(k - 1, F))  # Random coefficients.

    def f_(x):  # Polynomial definition of the form:  f(x) = S + a_1x + a_2x^2 + ... + a_k x^k
        res = 0
        for i, a in enumerate(as_):
            res = F_add(res, F_mul(a, pow(x, i, F), F), F)
        return res

    shares = [(i, f_(i)) for i in range(1, N + 1)]  # (1, f(1)), ..., (N, f(N))
    return shares


def reconstruct(shares: [], degree, x, F=F) -> int:
    """
    Reconstruct the polynomial from.
    :param shares: List of shares. **Shares**: (i, f(i)). **Invariance**: 1. Len(shares) >= degree + 1, 2. i is unique, 3. f(i) \in F.
    :param degree: The degree of the polynomial.
    :param x: The x value to evaluate the polynomial at.
    :return: F(0) - The secret.
    """
    k = degree + 1

    if len(shares) < k:
        raise ValueError("Not enough shares to reconstruct the polynomial.")

    secret = 0

    # Lagrange interpolation
    for i in range(k): 
        x_i, f_i = shares[i]
        y_i = 1
        for j in range(k):  
            if i == j:
                continue
            x_j, _ = shares[j]
            y_i = F_mul(F_div(F_sub(x, x_j, F), F_sub(x_i, x_j, F), F), y_i, F)

        y_i = F_mul(y_i, f_i, F)
        secret = F_add(secret, y_i, F) 

    return secret 


def test():
    # Assertions
    # Field operations
    assert F_add(1, 2) == 3
    assert F_sub(1, 2) == F - 1
    assert F_mul(2, 3) == 6

    # Split secret
    shares = split_secret(42, 5, 3)
    assert len(shares) == 5  # split_secret return N shares.
    assert all([1 <= i <= 5 for i, _ in shares])  # Shares are deterministic and in range
    assert all([a <= F for a in sample_coefficients(5)])  # Random coefficients are in range.

    # Reconstruct secret
    assert reconstruct(shares[:3], 2, 0) == 42  # Reconstruct the secret from the shares.
    assert reconstruct(SHARES, 2, 1) == SHARE_1  # Reconstruct the secret from the shares.
    
    #Check we can reconstruct SHARE_4 using constructed SHARE_0 with SHARE_1 and SHARE_2
    assert reconstruct([(0, reconstruct(SHARES, 2, 0)), (1, SHARE_1), (2, SHARE_2)], 2, 4) == SHARE_4
    

if __name__ == '__main__':
    test()

    S = 42
    shares = split_secret(S, 5, 3, 101)
    assert reconstruct(shares[:5], 2, 0, 101) == S
    print(shares)

    # Plot the shares as points.
    plt.scatter([0] + [i for i, _ in shares], [S] + [f for _, f in shares])
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.show()

    share_0 = reconstruct(SHARES, 2, 0)
    print("The reconstructed secret is: ", hex(share_0)[2:])
