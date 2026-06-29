import unittest
from mechanics_prototype import PsycheSystem

class TestPsycheSystemUpdate(unittest.TestCase):
	"""
	Unit tests for the update method of the PsycheSystem, focusing on
	the resonance drift calculation.
	"""

	def setUp(self):
		"""
		Create a fresh instance of the PsycheSystem before each test
		to ensure test isolation.
		"""
		self.system = PsycheSystem()

	def test_resonance_drifts_towards_shadow_with_spires(self):
		"""
		Verify that resonance increases (drifts to Shadow) when Spires are present.
		"""
		# Arrange: Initial resonance is 50. Build one spire.
		self.system.structures["spire"] = 1
		initial_resonance = self.system.resonance

		# Act: Run the update tick.
		self.system.update()

		# Assert: Resonance should increase by the pull strength * drift rate.
		# Expected: 50.0 + (1 spire * 1.0 pull) * 0.1 rate = 50.1
		expected_resonance = initial_resonance + (self.system.SPIRE_PULL_STRENGTH * self.system.RESONANCE_DRIFT_RATE)
		self.assertAlmostEqual(self.system.resonance, expected_resonance)

	def test_resonance_drifts_towards_light_with_sanctums(self):
		"""
		Verify that resonance decreases (drifts to Light) when Sanctums are present.
		"""
		# Arrange: Initial resonance is 50. Build two sanctums.
		self.system.structures["sanctum"] = 2
		initial_resonance = self.system.resonance

		# Act: Run the update tick.
		self.system.update()

		# Assert: Resonance should decrease by the pull strength * drift rate.
		# Expected: 50.0 - (2 sanctums * 1.0 pull) * 0.1 rate = 49.8
		expected_resonance = initial_resonance - (2 * self.system.SANCTUM_PULL_STRENGTH * self.system.RESONANCE_DRIFT_RATE)
		self.assertAlmostEqual(self.system.resonance, expected_resonance)

	def test_resonance_is_stable_with_balanced_forces(self):
		"""
		Verify that resonance does not drift when Light and Shadow pulls are equal.
		"""
		# Arrange: Initial resonance is 50. Build one of each structure.
		self.system.structures["spire"] = 1
		self.system.structures["sanctum"] = 1
		initial_resonance = self.system.resonance

		# Act: Run the update tick.
		self.system.update()

		# Assert: Resonance should not change.
		self.assertAlmostEqual(self.system.resonance, initial_resonance)

	def test_resonance_clamps_at_max_value(self):
		"""
		Verify that resonance does not exceed 100.
		"""
		# Arrange: Set resonance close to the max and build many spires.
		self.system.resonance = 99.95
		self.system.structures["spire"] = 10 # A strong pull

		# Act: Run the update tick.
		self.system.update()

		# Assert: Resonance should be clamped at exactly 100.0.
		self.assertEqual(self.system.resonance, 100.0)

	def test_resonance_clamps_at_min_value(self):
		"""
		Verify that resonance does not go below 0.
		"""
		# Arrange: Set resonance close to the min and build many sanctums.
		self.system.resonance = 0.05
		self.system.structures["sanctum"] = 10 # A strong pull

		# Act: Run the update tick.
		self.system.update()

		# Assert: Resonance should be clamped at exactly 0.0.
		self.assertEqual(self.system.resonance, 0.0)

if __name__ == '__main__':
	unittest.main()
