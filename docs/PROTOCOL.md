# BB84 Quantum Key Distribution Protocol

Complete explanation of the Bennett & Brassard (1984) quantum key distribution protocol.

## 📚 Overview

The BB84 protocol is a quantum cryptography protocol that allows two parties (Alice and Bob) to establish a shared secret key using quantum communication. It's the first practical quantum cryptography protocol and provides information-theoretic security against eavesdropping.

**Key Property**: Any attempt to intercept or measure the quantum states will be detected with high probability.

---

## 🔬 Quantum Foundations

### Qubits and Bases

A quantum bit (qubit) can be measured in different **bases**:

#### Rectilinear Basis (Z-basis)
- Represents bits as: |0⟩ and |1⟩
- States are orthogonal (distinguishable)
- Classical basis

#### Diagonal Basis (X-basis)
- Represents bits as: |+⟩ = (|0⟩ + |1⟩)/√2 and |−⟩ = (|0⟩ − |1⟩)/√2
- States are orthogonal in this basis
- Diagonal basis

### Measurement Problem

If you measure a qubit in the **wrong basis**:
- You get a 50% chance of each outcome
- The qubit state collapses (changes!)
- You cannot determine the original state

**This is the heart of the security.**

---

## 🔐 The 6-Step Protocol

### Step 1: Alice Prepares Qubits

Alice generates:
1. **Random bits**: b₁, b₂, ..., bₙ (the message she wants to send)
2. **Random bases**: θ₁, θ₂, ..., θₙ (Z or X basis for each bit)

For each bit-base pair:
- If bit=0 and basis=Z: prepare |0⟩
- If bit=1 and basis=Z: prepare |1⟩
- If bit=0 and basis=X: prepare |+⟩
- If bit=1 and basis=X: prepare |−⟩

**Example:**
```
Bits:   1 0 1 0 1 1 0 1
Bases:  Z X Z X X Z X Z
States: |1⟩|+⟩|1⟩|−⟩|−⟩|1⟩|+⟩|1⟩
```

### Step 2: Quantum Transmission

Alice sends all qubits to Bob through a quantum channel.

**Possible Interference:**
- Eve (eavesdropper) may intercept some/all qubits
- Eve must measure in a random basis (doesn't know correct basis)
- Eve's measurements collapse the states
- If Eve guesses wrong basis: 50% chance of changing the qubit state

### Step 3: Bob Measures

Bob receives the qubits and:
1. Generates random bases: θ'₁, θ'₂, ..., θ'ₙ
2. Measures each qubit in his chosen basis
3. Records his measurement results: b'₁, b'₂, ..., b'ₙ

**Measurement outcomes:**
- If Bob's basis matches Alice's: He gets the correct bit (50% overlap)
- If Bob's basis differs: He gets random result (50% overlap)

### Step 4: Basis Sifting (Public Channel)

Alice and Bob publicly compare bases (but NOT the measurement results):

```
Alice's bases:  Z X Z X X Z X Z
Bob's bases:    X Z Z X X Z X X
Match:          ✗ ✗ ✓ ✗ ✓ ✓ ✓ ✗

Sifted indices: [2, 4, 5, 6]
Sifted key:     [1, 1, 1, 0]
```

**Result:**
- ~50% of bits match and are kept
- ~50% are discarded
- This becomes the potential shared key

### Step 5: Error Estimation (QBER Check)

Alice and Bob publicly compare a random subset of sifted bits to check for errors:

```
Sifted key:     [1, 1, 1, 0, 1, 0, 1, 1]
Check indices:  [0, 3, 7]  (publicly revealed)
Alice's bits:   [1, 0, 1]
Bob's bits:     [1, 0, 1]
Errors:         0 (0%)

QBER = errors_found / bits_checked = 0%
```

**Interpretation:**
- **No error (QBER ≈ 0%)**: Channel is secure, no eavesdropper
- **High error (QBER > 11%)**: Likely eavesdropping detected
- **Threshold**: 11% (theoretical: 25% with 50% intercept rate)

### Step 6: Privacy Amplification

The remaining bits (not used for error checking) become the **final shared secret key**.

```
Sifted key:      [1, 1, 1, 0, 1, 0, 1, 1]
Checked bits:    [0, 3, 7]
Final key:       [1, 1, 0, 0, 1]  (indices 1,2,4,5,6)
Final key length: 5 bits
```

---

## 🛡️ Security Analysis

### Why Eavesdropping is Detected

**Scenario: Eve intercepts 50% of qubits**

1. Eve measures each intercepted qubit in a random basis
2. Eve guesses correctly 50% of the time
3. When Eve guesses wrong: She collapses the qubit to wrong state
4. Bob later measures and gets wrong result
5. This creates detectable errors

**Math:**
- Eve intercepts 50% of qubits
- Eve measures correctly 50% of those: 0.5 × 0.5 = 25% correct
- Eve measures incorrectly 50% of those: 0.5 × 0.5 = 25% incorrect
- Of Eve's incorrect 25%: Bob measures correctly 50% of time: 0.25 × 0.5 = 12.5% error
- **Expected QBER with 50% intercept**: 12.5% (> 11% threshold!)

### Information-Theoretic Security

- Security doesn't depend on computational hardness
- Security comes from **laws of quantum mechanics**
- Perfect security (Shannon's definition) is achievable

### Limitations

1. **Quantum Channel Quality**: Real channels have natural noise
2. **Detector Efficiency**: Not all photons are detected
3. **Source Quality**: Sources may have imperfections
4. **Practical Vulnerabilities**: Side-channel attacks on devices

---

## 📊 Performance Metrics

### Efficiency

**Sifting Efficiency**: ~50%
```
Starting bits: 1024
After sifting: ~512
Final key: 256 bits
```

**Key Generation Rate**: 25%
```
Final bits / Initial bits = 256 / 1024 = 25%
```

### Error Rate

**Quantum Bit Error Rate (QBER)**:
```
QBER = (errors_found / bits_checked) × 100%

- No eavesdropper: QBER ≈ 0-1% (channel noise)
- 50% eavesdropper: QBER ≈ 12.5% (detectable!)
- 100% eavesdropper: QBER ≈ 25% (always detectable)
```

### Security Threshold

**QBER Threshold: 11%**

```
QBER < 11%  ✓ Channel is SECURE
QBER ≥ 11%  ⚠️ Eavesdropping DETECTED → Abort
```

---

## 🖥️ Implementation Details

### Qubit Representation

In our implementation, qubits are represented classically:

```python
# Qubit in Z-basis (|0⟩ or |1⟩)
z_basis_bit = 0  # |0⟩
z_basis_bit = 1  # |1⟩

# Qubit in X-basis (|+⟩ or |−⟩)
x_basis_0 = random()  # 50/50 chance 0 or 1 when measured in X
x_basis_1 = random()  # 50/50 chance 0 or 1 when measured in X
```

### Measurement

```python
def measure_qubit(qubit_state, prepare_basis, measure_basis):
    if prepare_basis == measure_basis:
        # Correct basis: always get the original bit
        return qubit_state
    else:
        # Wrong basis: 50/50 random result
        return random(0, 1)  # 0 or 1 with equal probability
```

---

## 🔄 Protocol Variations

### BB84 Variants

1. **SARG04**: Enhanced variant with 4-state protocol
2. **Decoy-state BB84**: Uses decoy photons to prevent attacks
3. **Twin-Field QKD**: Extended range variant
4. **Device-Independent QKD**: No assumptions about devices

### Eve's Attack Strategies

1. **Intercept-Resend**: Eve intercepts and measures
2. **Entanglement-Based**: Eve uses entangled states
3. **Collective Attack**: Eve waits until end to analyze all data

---

## 📈 QBER Analysis Table

| Eve Intercept % | Expected QBER % | Detection |
|-----------------|-----------------|-----------|
| 0% (None)       | 0.0-1.0%        | ✓ Secure |
| 10%             | 2.5%            | ✓ Secure |
| 20%             | 5.0%            | ✓ Secure |
| 30%             | 7.5%            | ✓ Secure |
| 40%             | 10.0%           | ✓ Secure |
| 50%             | 12.5%           | ⚠️ Detected |
| 75%             | 18.75%          | ⚠️ Detected |
| 100%            | 25.0%           | ⚠️ Detected |

---

## 💡 Key Insights

1. **Randomness is Essential**: Both Alice and Bob must use true random bases
2. **Public Channel Needed**: Basis comparison must be public (not eavesdropping-safe but integrity-safe)
3. **Measurement Limits**: Eve cannot copy unknown quantum states
4. **Statistical Detection**: Need enough sifted bits to detect eavesdropping statistically
5. **No Assumptions**: Works without assumptions about Eve's computational power

---

## 📚 Further Reading

- Bennett & Brassard (1984). "Quantum cryptography: Public key distribution and coin tossing"
- Nielsen & Chuang. "Quantum Computation and Quantum Information" (Chapter 12)
- Brunner et al. (2014). "Bell nonlocality" (device-independent perspective)
- Arnon-Friedman et al. "Simple and tight device-independent security proofs"

---

## 🎯 Common Questions

### Q: Can Eve copy the quantum state to analyze later?
**A**: No! The No-Cloning Theorem forbids this. Quantum states cannot be perfectly copied.

### Q: What if Eve measures in the correct basis?
**A**: Eve still doesn't know the correct basis beforehand (it's random). She guesses and is right 50% of the time.

### Q: Why not use one basis for everything?
**A**: Because then Eve would always guess correctly, and no eavesdropping would be detectable.

### Q: Is this unbreakable?
**A**: Theoretically yes (information-theoretically secure). Practically, vulnerabilities exist in implementations.

### Q: Can Alice and Bob detect Eve before establishing the key?
**A**: No, but they can detect Eve before trusting the key. If QBER is high, they discard the key.
